from __future__ import annotations

import json
from datetime import UTC, datetime
from typing import Any

import boto3


class S3ReceiptStore:
    def __init__(self, bucket: str, region_name: str) -> None:
        self.bucket = bucket
        self.client = boto3.client("s3", region_name=region_name)

    def put_receipt(self, remittance_id: str, payload: dict[str, Any]) -> str:
        date_prefix = datetime.now(UTC).strftime("%Y/%m/%d")
        key = f"receipts/{date_prefix}/{remittance_id}.json"
        self.client.put_object(
            Bucket=self.bucket,
            Key=key,
            Body=json.dumps(payload, default=str).encode("utf-8"),
            ContentType="application/json",
            ServerSideEncryption="AES256",
        )
        return key
