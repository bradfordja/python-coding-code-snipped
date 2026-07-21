# Remitted Payments Lambda Sample

This sample shows a reusable Python package structure for an AWS Lambda workflow that processes remitted payments through a third-party payment API.

It demonstrates:

- AWS Lambda handler
- SNS event ingestion and SNS publishing
- IAM caller identity lookup
- S3 receipt/audit storage
- RDS persistence through PostgreSQL
- Redis caching/idempotency strategy
- Third-party payment API client abstraction
- Reusable package structure with dependency injection

## Architecture

```txt
SNS / API Gateway
  -> Lambda handler
    -> PaymentProcessingService
      -> Redis idempotency/cache
      -> RDS payment repository
      -> Third-party payment API
      -> S3 receipt storage
      -> SNS notification publishing
      -> IAM caller identity lookup for audit context
```

## Package Structure

```txt
python-payment-lambda/
  pyproject.toml
  template.yaml
  src/remittance_processor/
    lambda_handler.py
    config.py
    models.py
    services/payment_service.py
    aws/iam_client.py
    aws/s3_client.py
    aws/sns_client.py
    cache/redis_cache.py
    db/rds_repository.py
    external/payment_api.py
  tests/
    test_payment_service.py
```

## Local Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

## Lambda Environment Variables

```txt
AWS_REGION=us-east-1
PAYMENT_EVENTS_TOPIC_ARN=arn:aws:sns:us-east-1:123456789012:payment-events
PAYMENT_RECEIPT_BUCKET=my-payment-receipts
PAYMENT_API_BASE_URL=https://payments.example.com
PAYMENT_API_KEY=replace-me
REDIS_HOST=my-cache.xxxxxx.ng.0001.use1.cache.amazonaws.com
REDIS_PORT=6379
REDIS_TLS=true
RDS_HOST=mydb.xxxxxx.us-east-1.rds.amazonaws.com
RDS_PORT=5432
RDS_DB_NAME=payments
RDS_USER=payments_app
RDS_PASSWORD=replace-me
```

## Example SNS Message

```json
{
  "remittance_id": "remit_1001",
  "payer_id": "payer_abc",
  "payee_id": "payee_xyz",
  "amount": "1250.00",
  "currency": "USD",
  "invoice_id": "INV-2026-1001",
  "third_party_account_id": "acct_123",
  "metadata": {
    "source": "lockbox",
    "batch_id": "batch_789"
  }
}
```

## Security Notes

- This sample shows JWT/API-key-style outbound payment API authentication through an API key header. In production, prefer OAuth client credentials, mTLS, or signed requests if the provider supports them.
- Store secrets in AWS Secrets Manager or SSM Parameter Store, not plain Lambda environment variables.
- Redis is used for idempotency and short-lived payment status caching.
- RDS is the source of truth.
- S3 stores immutable payment receipts/audit payloads.
- SNS publishes success/failure events to downstream systems.
- IAM permissions should be least privilege and scoped to the exact topic, bucket, and secret resources.

## Deployment Sketch

The included `template.yaml` is a starter AWS SAM template. It intentionally leaves networking, VPC, Secrets Manager, RDS, and ElastiCache provisioning as placeholders because those vary heavily by account.
