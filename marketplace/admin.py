from django.contrib import admin
from .models import UserProfile, Product, Order, Category, HSNCode, FarmerProfile, BusinessProfile, ProductReview, UserReview

@admin.action(description='Block selected users')
def block_users(modeladmin, request, queryset):
    queryset.update(is_blocked=True)
    # Also update the related User model to prevent login
    for profile in queryset:
        profile.user.is_active = False
        profile.user.save()

@admin.action(description='Unblock selected users')
def unblock_users(modeladmin, request, queryset):
    queryset.update(is_blocked=False)
    for profile in queryset:
        profile.user.is_active = True
        profile.user.save()

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'buyer', 'product', 'quantity', 'grand_total', 'status', 'created_at')
    readonly_fields = ('sub_total', 'cgst_amount', 'sgst_amount', 'igst_amount', 'grand_total', 'tax_rate_applied', 'tax_type')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'farmer', 'category', 'hsn_code', 'price_per_unit', 'is_active')

class FarmerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'state', 'city', 'is_blocked')
    search_fields = ('user__username', 'full_name', 'city')
    list_filter = ('is_blocked', 'state')
    actions = [block_users, unblock_users]
    
    def get_queryset(self, request):
        return super().get_queryset(request).filter(role__in=['farmer', 'both'])

class BusinessProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'state', 'city', 'is_blocked')
    search_fields = ('user__username', 'full_name', 'city')
    list_filter = ('is_blocked', 'state')
    actions = [block_users, unblock_users]
    
    def get_queryset(self, request):
        return super().get_queryset(request).filter(role__in=['business', 'both'])

admin.site.register(FarmerProfile, FarmerProfileAdmin)
admin.site.register(BusinessProfile, BusinessProfileAdmin)
admin.site.register(Category)
admin.site.register(HSNCode)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(ProductReview)
admin.site.register(UserReview)