from django import forms
from .models import Product, Order

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "description", "price_per_unit", "unit", "available_quantity", "is_active"]

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["quantity"]