from __future__ import annotations

import json
from typing import Any

import boto3


class SnsPublisher:
    def __init__(self, topic_arn: str, region_name: str) -> None:
        self.topic_arn = topic_arn
        self.client = boto3.client("sns", region_name=region_name)

    def publish_payment_event(self, event_type: str, detail: dict[str, Any]) -> None:
        self.client.publish(
            TopicArn=self.topic_arn,
            Subject=event_type,
            Message=json.dumps({"event_type": event_type, "detail": detail}, default=str),
            MessageAttributes={
                "event_type": {
                    "DataType": "String",
                    "StringValue": event_type,
                }
            },
        )
