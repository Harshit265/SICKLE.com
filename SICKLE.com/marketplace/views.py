from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.db import transaction

from .models import Product, Order
from .forms import ProductForm, OrderForm

def home(request):
    return render(request, "home.html")

def product_list(request):
    products = Product.objects.filter(is_active=True).order_by("-created_at")
    return render(request, "product_list.html", {"products": products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk, is_active=True)
    return render(request, "product_detail.html", {"product": product})

@login_required
def product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.farmer = request.user
            product.save()
            return redirect("dashboard")
    else:
        form = ProductForm()
    return render(request, "product_create.html", {"form": form})

@login_required
def dashboard(request):
    my_products = Product.objects.filter(farmer=request.user).order_by("-created_at")
    my_orders = Order.objects.filter(buyer=request.user).order_by("-created_at")
    return render(request, "dashboard.html", {"my_products": my_products, "my_orders": my_orders})

@login_required
def order_create(request, product_pk):
    product = get_object_or_404(Product, pk=product_pk, is_active=True)
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            qty = form.cleaned_data["quantity"]
            if qty <= 0:
                form.add_error("quantity", "Quantity must be greater than 0.")
            elif qty > product.available_quantity:
                form.add_error("quantity", "Not enough stock available.")
            else:
                with transaction.atomic():
                    product.available_quantity = product.available_quantity - qty
                    product.save(update_fields=["available_quantity"])

                    Order.objects.create(
                        product=product,
                        buyer=request.user,
                        quantity=qty,
                    )
                return redirect("dashboard")
    else:
        form = OrderForm()
    return render(request, "order_create.html", {"product": product, "form": form})