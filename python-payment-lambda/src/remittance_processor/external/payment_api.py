from __future__ import annotations

import requests

from remittance_processor.models import PaymentResult, RemittancePayment


class ThirdPartyPaymentApiClient:
    def __init__(self, base_url: str, api_key: str) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key

    def submit_payment(self, payment: RemittancePayment, idempotency_key: str) -> PaymentResult:
        response = requests.post(
            f"{self.base_url}/v1/remitted-payments",
            json=payment.to_dict(),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Idempotency-Key": idempotency_key,
                "Content-Type": "application/json",
            },
            timeout=10,
        )

        if response.status_code >= 500:
            raise RuntimeError(f"Payment provider unavailable: {response.status_code}")

        body = response.json()

        if response.status_code >= 400:
            return PaymentResult(
                remittance_id=payment.remittance_id,
                status="failed",
                message=body.get("message", "Payment provider rejected the payment"),
            )

        return PaymentResult(
            remittance_id=payment.remittance_id,
            status="succeeded",
            provider_payment_id=body.get("payment_id"),
            message=body.get("message", "Payment accepted"),
        )
