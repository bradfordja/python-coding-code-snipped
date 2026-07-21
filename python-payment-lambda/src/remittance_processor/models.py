from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from typing import Any, Literal

PaymentStatus = Literal["received", "processing", "succeeded", "failed", "duplicate"]


@dataclass(frozen=True)
class RemittancePayment:
    remittance_id: str
    payer_id: str
    payee_id: str
    amount: Decimal
    currency: str
    invoice_id: str
    third_party_account_id: str
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "RemittancePayment":
        return cls(
            remittance_id=str(value["remittance_id"]),
            payer_id=str(value["payer_id"]),
            payee_id=str(value["payee_id"]),
            amount=Decimal(str(value["amount"])),
            currency=str(value["currency"]),
            invoice_id=str(value["invoice_id"]),
            third_party_account_id=str(value["third_party_account_id"]),
            metadata=dict(value.get("metadata", {})),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "remittance_id": self.remittance_id,
            "payer_id": self.payer_id,
            "payee_id": self.payee_id,
            "amount": str(self.amount),
            "currency": self.currency,
            "invoice_id": self.invoice_id,
            "third_party_account_id": self.third_party_account_id,
            "metadata": self.metadata,
        }


@dataclass(frozen=True)
class PaymentResult:
    remittance_id: str
    status: PaymentStatus
    provider_payment_id: str | None = None
    message: str | None = None
    receipt_s3_key: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "remittance_id": self.remittance_id,
            "status": self.status,
            "provider_payment_id": self.provider_payment_id,
            "message": self.message,
            "receipt_s3_key": self.receipt_s3_key,
        }
