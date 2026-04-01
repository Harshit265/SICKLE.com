from django.contrib import admin
from .models import UserProfile, Product, Order, Category, HSNCode, FarmerProfile, BusinessProfile

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'buyer', 'product', 'quantity', 'grand_total', 'status', 'created_at')
    readonly_fields = ('sub_total', 'cgst_amount', 'sgst_amount', 'igst_amount', 'grand_total', 'tax_rate_applied', 'tax_type')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'farmer', 'category', 'hsn_code', 'price_per_unit', 'is_active')

class FarmerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'state', 'city')
    search_fields = ('user__username', 'full_name', 'city')
    
    def get_queryset(self, request):
        return super().get_queryset(request).filter(role__in=['farmer', 'both'])

class BusinessProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'state', 'city')
    search_fields = ('user__username', 'full_name', 'city')
    
    def get_queryset(self, request):
        return super().get_queryset(request).filter(role__in=['business', 'both'])

admin.site.register(FarmerProfile, FarmerProfileAdmin)
admin.site.register(BusinessProfile, BusinessProfileAdmin)
admin.site.register(Category)
admin.site.register(HSNCode)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)