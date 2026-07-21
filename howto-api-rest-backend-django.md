# Standard Django REST API backend demo.
1. API Endpoint Design
```sh
POST    /api/auth/login/
POST    /api/auth/refresh/

GET     /api/customers/
POST    /api/customers/
GET     /api/customers/{id}/
PUT     /api/customers/{id}/
PATCH   /api/customers/{id}/
DELETE  /api/customers/{id}/

GET     /api/accounts/
POST    /api/accounts/
GET     /api/accounts/{id}/

GET     /api/transactions/
POST    /api/transactions/

GET     /api/customers/{id}/activity/
GET     /api/health/
```
⸻

2. Project Structure
```sh
backend/
  config/
    settings.py
    urls.py

  apps/
    customers/
      models.py
      serializers.py
      views.py
      urls.py

    accounts/
      models.py
      serializers.py
      views.py
      urls.py

    transactions/
      models.py
      serializers.py
      views.py
      urls.py

    health/
      views.py
      urls.py
```
⸻

3. Customer Model
# apps/customers/models.py
```py
from django.db import models

class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=30, blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ("ACTIVE", "Active"),
            ("INACTIVE", "Inactive"),
            ("SUSPENDED", "Suspended"),
        ],
        default="ACTIVE"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
```
⸻

4. Account Model
# apps/accounts/models.py
```py
from django.db import models
from apps.customers.models import Customer

class Account(models.Model):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="accounts"
    )
    account_number = models.CharField(max_length=50, unique=True)
    account_type = models.CharField(
        max_length=20,
        choices=[
            ("CHECKING", "Checking"),
            ("SAVINGS", "Savings"),
        ]
    )
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    currency = models.CharField(max_length=3, default="USD")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.account_number
```
⸻

5. Transaction Model
# apps/transactions/models.py
```py
from django.db import models
from apps.accounts.models import Account

class Transaction(models.Model):
    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name="transactions"
    )
    transaction_type = models.CharField(
        max_length=20,
        choices=[
            ("DEPOSIT", "Deposit"),
            ("WITHDRAWAL", "Withdrawal"),
            ("TRANSFER", "Transfer"),
        ]
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.CharField(max_length=255, blank=True, null=True)
    reference_number = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
```
⸻

6. Customer Serializer
# apps/customers/serializers.py
```py
from rest_framework import serializers
from .models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = [
            "id",
            "first_name",
            "last_name",
            "full_name",
            "email",
            "phone_number",
            "status",
            "created_at",
        ]

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
```
⸻

7. Account Serializer
# apps/accounts/serializers.py
```py
from rest_framework import serializers
from .models import Account

class AccountSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(
        source="customer.__str__",
        read_only=True
    )

    class Meta:
        model = Account
        fields = [
            "id",
            "customer",
            "customer_name",
            "account_number",
            "account_type",
            "balance",
            "currency",
            "created_at",
        ]
```
⸻

8. Transaction Serializer
# apps/transactions/serializers.py
```py
from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = [
            "id",
            "account",
            "transaction_type",
            "amount",
            "description",
            "reference_number",
            "created_at",
        ]

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value
```
⸻

9. Customer ViewSet
# apps/customers/views.py
```py
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .models import Customer
from .serializers import CustomerSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]

    queryset = Customer.objects.all().order_by("-created_at")

    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    search_fields = [
        "first_name",
        "last_name",
        "email",
        "phone_number",
    ]

    ordering_fields = [
        "created_at",
        "last_name",
        "status",
    ]
```
This gives you:
```sh
GET     /api/customers/
POST    /api/customers/
GET     /api/customers/1/
PUT     /api/customers/1/
PATCH   /api/customers/1/
DELETE  /api/customers/1/
# Search example:
GET /api/customers/?search=john
# Ordering example:
GET /api/customers/?ordering=last_name
```
⸻

10. Account ViewSet
# apps/accounts/views.py
```py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Account
from .serializers import AccountSerializer

class AccountViewSet(viewsets.ModelViewSet):
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Account.objects.select_related("customer").all()

        customer_id = self.request.query_params.get("customer_id")

        if customer_id:
            queryset = queryset.filter(customer_id=customer_id)

        return queryset.order_by("-created_at")

# Example:
## sh
## GET /api/accounts/?customer_id=1
```
⸻

11. Transaction ViewSet
# apps/transactions/views.py
```py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Transaction
from .serializers import TransactionSerializer

class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Transaction.objects.select_related("account").all()

        account_id = self.request.query_params.get("account_id")

        if account_id:
            queryset = queryset.filter(account_id=account_id)

        return queryset.order_by("-created_at")
# Example:
# GET /api/transactions/?account_id=10
```
⸻

12. URLs with Router
# apps/customers/urls.py
```py
from rest_framework.routers import DefaultRouter
from .views import CustomerViewSet

router = DefaultRouter()
router.register("", CustomerViewSet, basename="customers")

urlpatterns = router.urls
# apps/accounts/urls.py

from rest_framework.routers import DefaultRouter
from .views import AccountViewSet

router = DefaultRouter()
router.register("", AccountViewSet, basename="accounts")

urlpatterns = router.urls
# apps/transactions/urls.py

from rest_framework.routers import DefaultRouter
from .views import TransactionViewSet

router = DefaultRouter()
router.register("", TransactionViewSet, basename="transactions")

urlpatterns = router.urls
```
⸻

13. Main Django URL Config
# config/urls.py
```py
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("api/auth/login/", TokenObtainPairView.as_view()),
    path("api/auth/refresh/", TokenRefreshView.as_view()),

    path("api/customers/", include("apps.customers.urls")),
    path("api/accounts/", include("apps.accounts.urls")),
    path("api/transactions/", include("apps.transactions.urls")),
    path("api/health/", include("apps.health.urls")),
]
```
⸻

14. Health Check API
# apps/health/views.py
```py
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import connection

class HealthCheckView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            database_status = "UP"
        except Exception:
            database_status = "DOWN"

        return Response({
            "status": "UP",
            "database": database_status
        })
# apps/health/urls.py

from django.urls import path
from .views import HealthCheckView

urlpatterns = [
    path("", HealthCheckView.as_view()),
]
```
⸻

15. DynamoDB Customer Activity API
# apps/customers/dynamodb_service.py
```py
import boto3

dynamodb = boto3.resource(
    "dynamodb",
    region_name="us-east-1"
)

def get_customer_activity(customer_id):
    table = dynamodb.Table("CustomerActivity")

    response = table.query(
        KeyConditionExpression="customer_id = :customer_id",
        ExpressionAttributeValues={
            ":customer_id": str(customer_id)
        }
    )

    return response.get("Items", [])
# apps/customers/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .dynamodb_service import get_customer_activity

class CustomerActivityView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, customer_id):
        activity = get_customer_activity(customer_id)

        return Response({
            "customer_id": customer_id,
            "activity": activity
        })
Add this to customer URLs:
# apps/customers/urls.py

from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CustomerViewSet, CustomerActivityView

router = DefaultRouter()
router.register("", CustomerViewSet, basename="customers")

urlpatterns = [
    path("<int:customer_id>/activity/", CustomerActivityView.as_view()),
]

urlpatterns += router.urls
# Endpoint:
## GET /api/customers/1/activity/
```
⸻

16. Pagination Settings
# config/settings.py
```json
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
}
# Response example:
{
  "count": 100,
  "next": "http://localhost:8000/api/customers/?page=2",
  "previous": null,
  "results": []
}
```
⸻

17. Example Login Request
POST /api/auth/login/
Content-Type: application/json
```json
{
  "username": "admin",
  "password": "password123"
}
# Response:
{
  "refresh": "refresh-token-here",
  "access": "access-token-here"
}
```
⸻

18. Authenticated API Request
GET /api/customers/
Authorization: Bearer access-token-here

⸻

19. Example Create Customer Request
POST /api/customers/
Authorization: Bearer access-token-here
Content-Type: application/json
```json
{
  "first_name": "Julio",
  "last_name": "Bradford",
  "email": "julio@example.com",
  "phone_number": "555-111-2222",
  "status": "ACTIVE"
}
```
⸻

20. Example Create Account Request
POST /api/accounts/
Authorization: Bearer access-token-here
Content-Type: application/json
```json
{
  "customer": 1,
  "account_number": "ACCT-10001",
  "account_type": "CHECKING",
  "balance": "500.00",
  "currency": "USD"
}
```
⸻

21. Example Create Transaction Request
POST /api/transactions/
Authorization: Bearer access-token-here
Content-Type: application/json
```json
{
  "account": 1,
  "transaction_type": "DEPOSIT",
  "amount": "250.00",
  "description": "Initial deposit",
  "reference_number": "TXN-100001"
}
```
⸻

Senior-Level Summary
This gives you a standard Django REST backend with:
```sh
JWT authentication
CRUD APIs
PostgreSQL / Aurora models
Django ORM
DynamoDB integration
pagination
search
ordering
health check endpoint
secured APIs
clean app separation
For an enterprise system, this is a strong starting pattern because each Django app owns one business domain: customers, accounts, transactions, health, and integrations.
```