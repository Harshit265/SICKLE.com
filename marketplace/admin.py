from django.contrib import admin
from .models import UserProfile # Make sure this matches your models.py name

# Register your UserProfile
admin.site.register(UserProfile)

# COMMENT OUT these lines below until we actually create Product/Order models
# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     pass