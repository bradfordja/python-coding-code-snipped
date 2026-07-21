from __future__ import annotations

import psycopg

from remittance_processor.models import PaymentResult, RemittancePayment


class RdsPaymentRepository:
    def __init__(self, host: str, port: int, db_name: str, user: str, password: str) -> None:
        self.connection_info = {
            "host": host,
            "port": port,
            "dbname": db_name,
            "user": user,
            "password": password,
            "connect_timeout": 3,
        }

    def save_received(self, payment: RemittancePayment) -> None:
        with psycopg.connect(**self.connection_info) as conn:
            conn.execute(
                """
                insert into remittance_payments (
                    remittance_id, payer_id, payee_id, amount, currency,
                    invoice_id, third_party_account_id, status, metadata
                )
                values (%s, %s, %s, %s, %s, %s, %s, 'received', %s)
                on conflict (remittance_id) do nothing
                """,
                (
                    payment.remittance_id,
                    payment.payer_id,
                    payment.payee_id,
                    payment.amount,
                    payment.currency,
                    payment.invoice_id,
                    payment.third_party_account_id,
                    psycopg.types.json.Jsonb(payment.metadata),
                ),
            )

    def save_result(self, result: PaymentResult) -> None:
        with psycopg.connect(**self.connection_info) as conn:
            conn.execute(
                """
                update remittance_payments
                   set status = %s,
                       provider_payment_id = %s,
                       result_message = %s,
                       receipt_s3_key = %s,
                       updated_at = now()
                 where remittance_id = %s
                """,
                (
                    result.status,
                    result.provider_payment_id,
                    result.message,
                    result.receipt_s3_key,
                    result.remittance_id,
                ),
            )

    def find_result(self, remittance_id: str) -> PaymentResult | None:
        with psycopg.connect(**self.connection_info) as conn:
            row = conn.execute(
                """
                select remittance_id, status, provider_payment_id, result_message, receipt_s3_key
                  from remittance_payments
                 where remittance_id = %s
                   and status in ('succeeded', 'failed')
                """,
                (remittance_id,),
            ).fetchone()

        if row is None:
            return None

        return PaymentResult(
            remittance_id=row[0],
            status=row[1],
            provider_payment_id=row[2],
            message=row[3],
            receipt_s3_key=row[4],
        )
