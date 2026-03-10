from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255, blank=True)
    role = models.CharField(max_length=20) # 'farmer', 'business', or 'both'
    mobile_number = models.CharField(max_length=15, blank=True)
    state = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    address = models.TextField(blank=True)
    
    # Custom fields for SICKLE
    products_offered = models.TextField(blank=True, null=True) # For Farmers
    products_needed = models.TextField(blank=True, null=True)  # For Businesses

    def __str__(self):
        return f"{self.user.username} - {self.role}"


class Product(models.Model):
    farmer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="products"
    )
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price_per_unit = models.DecimalField(max_digits=12, decimal_places=2)
    unit = models.CharField(max_length=50, default="kg")
    available_quantity = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.farmer.username}"


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        CONFIRMED = "CONFIRMED", "Confirmed"
        FULFILLED = "FULFILLED", "Fulfilled"
        CANCELLED = "CANCELLED", "Cancelled"

    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    quantity = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_price(self):
        return self.quantity * self.product.price_per_unit

    def __str__(self):
        return f"Order #{self.id} - {self.product.name}"