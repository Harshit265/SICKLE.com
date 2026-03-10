from django.contrib import admin
from .models import UserProfile, Product, Order

admin.site.register(UserProfile)
admin.site.register(Product)
admin.site.register(Order)