from __future__ import annotations

from remittance_processor.models import PaymentResult, RemittancePayment
from remittance_processor.ports import (
    AuditIdentityProvider,
    CacheClient,
    EventPublisher,
    PaymentApiClient,
    PaymentRepository,
    ReceiptStore,
)


class PaymentProcessingService:
    def __init__(
        self,
        cache: CacheClient,
        repository: PaymentRepository,
        payment_api: PaymentApiClient,
        receipt_store: ReceiptStore,
        event_publisher: EventPublisher,
        audit_identity_provider: AuditIdentityProvider,
        idempotency_ttl_seconds: int,
        payment_status_ttl_seconds: int,
    ) -> None:
        self.cache = cache
        self.repository = repository
        self.payment_api = payment_api
        self.receipt_store = receipt_store
        self.event_publisher = event_publisher
        self.audit_identity_provider = audit_identity_provider
        self.idempotency_ttl_seconds = idempotency_ttl_seconds
        self.payment_status_ttl_seconds = payment_status_ttl_seconds

    def process(self, payment: RemittancePayment) -> PaymentResult:
        idempotency_key = f"remittance:{payment.remittance_id}"
        result_cache_key = f"{idempotency_key}:result"

        cached_result = self.cache.get_json(result_cache_key)
        if cached_result:
            return PaymentResult(**cached_result)

        if not self.cache.claim_idempotency_key(idempotency_key, self.idempotency_ttl_seconds):
            existing_result = self.repository.find_result(payment.remittance_id)
            if existing_result:
                self.cache.set_json(
                    result_cache_key,
                    existing_result.to_dict(),
                    self.payment_status_ttl_seconds,
                )
                return existing_result

            return PaymentResult(
                remittance_id=payment.remittance_id,
                status="duplicate",
                message="Payment is already being processed",
            )

        self.repository.save_received(payment)
        audit_identity = self.audit_identity_provider.caller_identity()

        try:
            result = self.payment_api.submit_payment(payment, idempotency_key)
            receipt_key = self.receipt_store.put_receipt(
                payment.remittance_id,
                {
                    "payment": payment.to_dict(),
                    "result": result.to_dict(),
                    "audit_identity": audit_identity,
                },
            )
            result = PaymentResult(
                remittance_id=result.remittance_id,
                status=result.status,
                provider_payment_id=result.provider_payment_id,
                message=result.message,
                receipt_s3_key=receipt_key,
            )
        except Exception as exc:
            result = PaymentResult(
                remittance_id=payment.remittance_id,
                status="failed",
                message=str(exc),
            )

        self.repository.save_result(result)
        self.cache.set_json(result_cache_key, result.to_dict(), self.payment_status_ttl_seconds)
        self.event_publisher.publish_payment_event(f"payment.{result.status}", result.to_dict())

        return result
