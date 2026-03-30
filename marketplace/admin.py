from django.contrib import admin
from .models import UserProfile, Product, Order, Category, HSNCode

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'buyer', 'product', 'quantity', 'grand_total', 'status', 'created_at')
    readonly_fields = ('sub_total', 'cgst_amount', 'sgst_amount', 'igst_amount', 'grand_total', 'tax_rate_applied', 'tax_type')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'farmer', 'category', 'hsn_code', 'price_per_unit', 'is_active')

admin.site.register(UserProfile)
admin.site.register(Category)
admin.site.register(HSNCode)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)