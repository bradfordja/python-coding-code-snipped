from __future__ import annotations

from typing import Any

import boto3


class IamAuditClient:
    def __init__(self, region_name: str) -> None:
        self.client = boto3.client("sts", region_name=region_name)

    def caller_identity(self) -> dict[str, Any]:
        identity = self.client.get_caller_identity()
        return {
            "account": identity.get("Account"),
            "arn": identity.get("Arn"),
            "user_id": identity.get("UserId"),
        }
