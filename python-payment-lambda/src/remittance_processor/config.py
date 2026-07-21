from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    aws_region: str
    payment_events_topic_arn: str
    payment_receipt_bucket: str
    payment_api_base_url: str
    payment_api_key: str
    redis_host: str
    redis_port: int
    redis_tls: bool
    rds_host: str
    rds_port: int
    rds_db_name: str
    rds_user: str
    rds_password: str
    idempotency_ttl_seconds: int = 60 * 60 * 24
    payment_status_ttl_seconds: int = 60 * 15

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            aws_region=os.getenv("AWS_REGION", "us-east-1"),
            payment_events_topic_arn=_required("PAYMENT_EVENTS_TOPIC_ARN"),
            payment_receipt_bucket=_required("PAYMENT_RECEIPT_BUCKET"),
            payment_api_base_url=_required("PAYMENT_API_BASE_URL"),
            payment_api_key=_required("PAYMENT_API_KEY"),
            redis_host=_required("REDIS_HOST"),
            redis_port=int(os.getenv("REDIS_PORT", "6379")),
            redis_tls=os.getenv("REDIS_TLS", "true").lower() == "true",
            rds_host=_required("RDS_HOST"),
            rds_port=int(os.getenv("RDS_PORT", "5432")),
            rds_db_name=_required("RDS_DB_NAME"),
            rds_user=_required("RDS_USER"),
            rds_password=_required("RDS_PASSWORD"),
        )


def _required(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value
