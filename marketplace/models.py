
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
    gst_number = models.CharField(max_length=15, blank=True)
    is_blocked = models.BooleanField(default=False)
    
    # Custom fields for Sickle.com
    products_offered = models.TextField(blank=True, null=True) # For Farmers
    products_needed = models.TextField(blank=True, null=True)  # For Businesses

    def __str__(self):
        return f"{self.user.username} - {self.role}"

class FarmerProfile(UserProfile):
    class Meta:
        proxy = True
        verbose_name = 'Farmer Profile'
        verbose_name_plural = 'Farmer Profiles'

class BusinessProfile(UserProfile):
    class Meta:
        proxy = True
        verbose_name = 'Business Profile'
        verbose_name_plural = 'Business Profiles'


class Category(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class HSNCode(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='hsn_codes')
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    igst_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.0, help_text="Total GST Rate (%) - IGST")
    cgst_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    sgst_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)

    def __str__(self):
        return f"{self.code} - {self.igst_rate}% GST"


class Product(models.Model):
    farmer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="products"
    )
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    hsn_code = models.ForeignKey(HSNCode, on_delete=models.SET_NULL, null=True, blank=True)
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
    
    # Billing fields
    sub_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    cgst_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    sgst_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    igst_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    grand_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tax_rate_applied = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    tax_type = models.CharField(max_length=20, blank=True) # "CGST+SGST" or "IGST"
    
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_price(self):
        return self.grand_total if self.grand_total > 0 else self.quantity * self.product.price_per_unit

    def __str__(self):
        return f"Order #{self.id} - {self.product.name}"


class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_given')
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.rating} star - {self.product.name} by {self.user.username}"


class UserReview(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_reviews_given')
    reviewee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_reviews_received')
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.rating} star for {self.reviewee.username} by {self.reviewer.username}"