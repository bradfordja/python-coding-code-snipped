from __future__ import annotations

from typing import Any, Protocol

from remittance_processor.models import PaymentResult, RemittancePayment


class CacheClient(Protocol):
    def claim_idempotency_key(self, key: str, ttl_seconds: int) -> bool:
        """Return true only for the first caller that claims a key."""

    def get_json(self, key: str) -> dict[str, Any] | None:
        """Return cached JSON data when present."""

    def set_json(self, key: str, value: dict[str, Any], ttl_seconds: int) -> None:
        """Cache JSON data with an expiration."""


class PaymentRepository(Protocol):
    def save_received(self, payment: RemittancePayment) -> None:
        """Persist a newly received remittance."""

    def save_result(self, result: PaymentResult) -> None:
        """Persist the final provider result."""

    def find_result(self, remittance_id: str) -> PaymentResult | None:
        """Return an existing result for duplicate/idempotent requests."""


class PaymentApiClient(Protocol):
    def submit_payment(self, payment: RemittancePayment, idempotency_key: str) -> PaymentResult:
        """Submit a remitted payment to the provider."""


class ReceiptStore(Protocol):
    def put_receipt(self, remittance_id: str, payload: dict[str, Any]) -> str:
        """Store payment receipt/audit data and return the S3 key."""


class EventPublisher(Protocol):
    def publish_payment_event(self, event_type: str, detail: dict[str, Any]) -> None:
        """Publish a payment event."""


class AuditIdentityProvider(Protocol):
    def caller_identity(self) -> dict[str, Any]:
        """Return execution identity for audit context."""
