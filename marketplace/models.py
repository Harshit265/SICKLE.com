from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.conf import settings
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20) # farmer, business, or both
    mobile_number = models.CharField(max_length=15)
    
    # New fields for the specific questions we added
    products_offered = models.TextField(blank=True, null=True) # For Farmers
    products_needed = models.TextField(blank=True, null=True)  # For Businesses

    def __str__(self):
        return f"{self.user.username} - {self.role}"


class Product(models.Model):
    farmer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
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
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders")
    quantity = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_price(self):
        return self.quantity * self.product.price_per_unit

    def __str__(self):
        return f"Order #{self.id} - {self.product.name}"
class UserProfile(models.Model):
    # Links to Django's built-in User system (Username/Password)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # Custom fields for SICKLE
    mobile_number = models.CharField(max_length=15)
    user_type = models.CharField(max_length=20) # Business, Farmer, or Both
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    address = models.TextField()
    
    # Store what they are looking for or providing
    product_info = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.user_type}"   