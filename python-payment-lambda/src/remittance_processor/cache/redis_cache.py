from __future__ import annotations

import json
from typing import Any

import redis


class RedisCache:
    def __init__(self, host: str, port: int, tls: bool) -> None:
        self.client = redis.Redis(
            host=host,
            port=port,
            ssl=tls,
            decode_responses=True,
            socket_connect_timeout=3,
            socket_timeout=3,
        )

    def claim_idempotency_key(self, key: str, ttl_seconds: int) -> bool:
        return bool(self.client.set(name=key, value="processing", nx=True, ex=ttl_seconds))

    def get_json(self, key: str) -> dict[str, Any] | None:
        raw = self.client.get(key)
        if raw is None:
            return None
        return json.loads(raw)

    def set_json(self, key: str, value: dict[str, Any], ttl_seconds: int) -> None:
        self.client.set(name=key, value=json.dumps(value), ex=ttl_seconds)
