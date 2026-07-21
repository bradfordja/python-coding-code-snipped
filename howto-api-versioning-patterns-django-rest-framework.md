API Versioning Patterns in Django REST Framework
API versioning lets you change your API without breaking existing clients.

Example:
```sh
/api/v1/bills/
/api/v2/bills/
```

Version v1 may return a simple bill response.Version v2 may add new fields, change validation, or improve response format.

⸻

Common Versioning Patterns
1. URL Path Versioning
Most common and interview-friendly.
```sh
/api/v1/bills/
/api/v2/bills/
```
Good because it is clear, easy to test, and easy for frontend/mobile teams to understand.

⸻

2. Query Parameter Versioning
```sh
/api/bills/?version=v1
/api/bills/?version=v2
```
Simple, but less clean for large systems.

⸻

3. Header Versioning
GET /api/bills/
Accept: application/json; version=v1
Cleaner URL, but harder to test and debug.

⸻

Django REST Framework Setup
settings.py
REST_FRAMEWORK = {
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.URLPathVersioning",
    "DEFAULT_VERSION": "v1",
    "ALLOWED_VERSIONS": ["v1", "v2"],
    "VERSION_PARAM": "version",
}

⸻

Models
# billing/models.py
```py
from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name
        
class Bill(models.Model):
    STATUS_CHOICES = [
        ("DRAFT", "Draft"),
        ("SENT", "Sent"),
        ("PAID", "Paid"),
        ("CANCELLED", "Cancelled"),
    ]

    customer = models.ForeignKey(
        Customer,
        related_name="bills",
        on_delete=models.CASCADE
    )
    bill_number = models.CharField(max_length=50, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="DRAFT")
    due_date = models.DateField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_amount(self):
        return self.amount + self.tax_amount

    def __str__(self):
        return self.bill_number
```
⸻

V1 Serializer
Simple version.
# billing/serializers.py
```py
from rest_framework import serializers
from .models import Bill


class BillV1Serializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = [
            "id",
            "bill_number",
            "customer",
            "amount",
            "status",
            "due_date",
        ]
```
⸻

V2 Serializer
More detailed version.
```py
class BillV2Serializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source="customer.name", read_only=True)
    customer_email = serializers.EmailField(source="customer.email", read_only=True)
    total_amount = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True
    )

    class Meta:
        model = Bill
        fields = [
            "id",
            "bill_number",
            "customer",
            "customer_name",
            "customer_email",
            "amount",
            "tax_amount",
            "total_amount",
            "status",
            "due_date",
            "created_at",
        ]
```
⸻

ViewSet with Version Logic
# billing/views.py
```py
from rest_framework import viewsets, permissions
from .models import Bill
from .serializers import BillV1Serializer, BillV2Serializer

class BillViewSet(viewsets.ModelViewSet):
    queryset = Bill.objects.select_related("customer").all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.version == "v2":
            return BillV2Serializer
        return BillV1Serializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
```
⸻

URLs
# project/urls.py
```py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from billing.views import BillViewSet

router = DefaultRouter()
router.register(r"bills", BillViewSet, basename="bills")

urlpatterns = [
    path("api/<str:version>/", include(router.urls)),
]
```
⸻

Example Requests
V1
GET /api/v1/bills/1/
Response:
```json
{
  "id": 1,
  "bill_number": "BILL-1001",
  "customer": 7,
  "amount": "250.00",
  "status": "SENT",
  "due_date": "2026-06-15"
}
```
⸻

V2
GET /api/v2/bills/1/
Response:
```json
{
  "id": 1,
  "bill_number": "BILL-1001",
  "customer": 7,
  "customer_name": "ABC Logistics",
  "customer_email": "billing@abclogistics.com",
  "amount": "250.00",
  "tax_amount": "20.00",
  "total_amount": "270.00",
  "status": "SENT",
  "due_date": "2026-06-15",
  "created_at": "2026-05-22T14:30:00Z"
}
```
⸻

Interview Answer
A strong answer:
In Django REST Framework, I usually prefer URL path versioning for enterprise APIs because it is explicit and easy for frontend, mobile, and external clients to consume. For example, /api/v1/bills/ and /api/v2/bills/. I keep the same ViewSet where possible and switch serializers based on request.version. If the business logic changes significantly, I separate the views by version. This allows old clients to continue using v1 while new clients can move to v2 safely.
