from django.contrib import admin
from .models import Profile, Product, Order

# Register the Profile model
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "company_or_farm_name", "location")
    search_fields = ("user__username", "company_or_farm_name", "location")
    list_filter = ("role",)

# Register the Product model
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "farmer", "price_per_unit", "unit", "available_quantity", "is_active", "created_at")
    search_fields = ("name", "farmer__username")
    list_filter = ("is_active", "unit")

# Register the Order model
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "buyer", "quantity", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("product__name", "buyer__username")