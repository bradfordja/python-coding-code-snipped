from __future__ import annotations

import unittest
from decimal import Decimal

from remittance_processor.models import PaymentResult, RemittancePayment
from remittance_processor.services.payment_service import PaymentProcessingService


class FakeCache:
    def __init__(self) -> None:
        self.values: dict[str, dict] = {}
        self.claimed: set[str] = set()

    def claim_idempotency_key(self, key: str, ttl_seconds: int) -> bool:
        if key in self.claimed:
            return False
        self.claimed.add(key)
        return True

    def get_json(self, key: str) -> dict | None:
        return self.values.get(key)

    def set_json(self, key: str, value: dict, ttl_seconds: int) -> None:
        self.values[key] = value


class FakeRepository:
    def __init__(self) -> None:
        self.results: dict[str, PaymentResult] = {}

    def save_received(self, payment: RemittancePayment) -> None:
        return None

    def save_result(self, result: PaymentResult) -> None:
        self.results[result.remittance_id] = result

    def find_result(self, remittance_id: str) -> PaymentResult | None:
        return self.results.get(remittance_id)


class FakePaymentApi:
    def submit_payment(self, payment: RemittancePayment, idempotency_key: str) -> PaymentResult:
        return PaymentResult(
            remittance_id=payment.remittance_id,
            status="succeeded",
            provider_payment_id="pay_123",
            message="Payment accepted",
        )


class FakeReceiptStore:
    def put_receipt(self, remittance_id: str, payload: dict) -> str:
        return f"receipts/{remittance_id}.json"


class FakeEventPublisher:
    def __init__(self) -> None:
        self.events: list[tuple[str, dict]] = []

    def publish_payment_event(self, event_type: str, detail: dict) -> None:
        self.events.append((event_type, detail))


class FakeAuditIdentityProvider:
    def caller_identity(self) -> dict:
        return {"account": "123456789012", "arn": "arn:aws:sts::123456789012:assumed-role/demo"}


class PaymentProcessingServiceTest(unittest.TestCase):
    def test_process_payment_success(self) -> None:
        cache = FakeCache()
        repository = FakeRepository()
        publisher = FakeEventPublisher()
        service = PaymentProcessingService(
            cache=cache,
            repository=repository,
            payment_api=FakePaymentApi(),
            receipt_store=FakeReceiptStore(),
            event_publisher=publisher,
            audit_identity_provider=FakeAuditIdentityProvider(),
            idempotency_ttl_seconds=86400,
            payment_status_ttl_seconds=900,
        )

        result = service.process(
            RemittancePayment(
                remittance_id="remit_1001",
                payer_id="payer_abc",
                payee_id="payee_xyz",
                amount=Decimal("1250.00"),
                currency="USD",
                invoice_id="INV-1001",
                third_party_account_id="acct_123",
            )
        )

        self.assertEqual(result.status, "succeeded")
        self.assertEqual(result.provider_payment_id, "pay_123")
        self.assertEqual(result.receipt_s3_key, "receipts/remit_1001.json")
        self.assertEqual(publisher.events[0][0], "payment.succeeded")


if __name__ == "__main__":
    unittest.main()
