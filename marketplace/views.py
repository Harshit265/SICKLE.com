from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .forms import RegistrationForm
from .models import Product, Order
from django.contrib.auth.models import User
from .models import UserProfile

def home(request):
    return render(request, "home.html")

def product_list(request):
    products = Product.objects.filter(is_active=True).order_by("-created_at")
    return render(request, "product_list.html", {"products": products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk, is_active=True)
    return render(request, "product_detail.html", {"product": product})


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


def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            
            # 1. Create the base User with their chosen password
            new_user = User.objects.create_user(
                username=data['email'], 
                email=data['email'],
                password=data['password'] # Securely hashed by Django automatically
            )
            
            # 2. Logic for product info
            info = data.get('business_needs') or data.get('farmer_provides') or ""

            # 3. Create the Profile
            UserProfile.objects.create(
                user=new_user,
                mobile_number=data['mobile_number'],
                # ... (rest of your fields) ...
                product_info=info
            )
            
            return redirect('login') # Send them to the login page now!
    else:
        form = RegistrationForm()
        
    return render(request, 'register.html', {'form': form})