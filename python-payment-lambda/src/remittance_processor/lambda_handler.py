from __future__ import annotations

import json
from typing import Any

from remittance_processor.aws.iam_client import IamAuditClient
from remittance_processor.aws.s3_client import S3ReceiptStore
from remittance_processor.aws.sns_client import SnsPublisher
from remittance_processor.cache.redis_cache import RedisCache
from remittance_processor.config import Settings
from remittance_processor.db.rds_repository import RdsPaymentRepository
from remittance_processor.external.payment_api import ThirdPartyPaymentApiClient
from remittance_processor.models import RemittancePayment
from remittance_processor.services.payment_service import PaymentProcessingService


def handler(event: dict[str, Any], context: Any) -> dict[str, Any]:
    service = build_service(Settings.from_env())
    payments = extract_payments(event)
    results = [service.process(payment).to_dict() for payment in payments]

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "request_id": getattr(context, "aws_request_id", None),
                "processed": len(results),
                "results": results,
            }
        ),
    }


def build_service(settings: Settings) -> PaymentProcessingService:
    return PaymentProcessingService(
        cache=RedisCache(settings.redis_host, settings.redis_port, settings.redis_tls),
        repository=RdsPaymentRepository(
            host=settings.rds_host,
            port=settings.rds_port,
            db_name=settings.rds_db_name,
            user=settings.rds_user,
            password=settings.rds_password,
        ),
        payment_api=ThirdPartyPaymentApiClient(
            base_url=settings.payment_api_base_url,
            api_key=settings.payment_api_key,
        ),
        receipt_store=S3ReceiptStore(settings.payment_receipt_bucket, settings.aws_region),
        event_publisher=SnsPublisher(settings.payment_events_topic_arn, settings.aws_region),
        audit_identity_provider=IamAuditClient(settings.aws_region),
        idempotency_ttl_seconds=settings.idempotency_ttl_seconds,
        payment_status_ttl_seconds=settings.payment_status_ttl_seconds,
    )


def extract_payments(event: dict[str, Any]) -> list[RemittancePayment]:
    if "Records" in event:
        return [
            RemittancePayment.from_dict(json.loads(record["Sns"]["Message"]))
            for record in event["Records"]
            if "Sns" in record
        ]

    if "body" in event:
        body = event["body"]
        payload = json.loads(body) if isinstance(body, str) else body
        return [RemittancePayment.from_dict(payload)]

    return [RemittancePayment.from_dict(event)]
