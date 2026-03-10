from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .forms import RegistrationForm
from .models import Product, Order, UserProfile
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login

def home(request):
    return render(request, 'home.html')

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            
            if User.objects.filter(username=data['email']).exists():
                messages.error(request, 'Email already exists.')
                return render(request, 'register.html', {'form': form})
            
            new_user = User.objects.create_user(
                username=data['email'], 
                email=data['email'],
                password=data['password']
            )
            
            UserProfile.objects.create(
                user=new_user,
                full_name=data['full_name'],
                role=data['role'],
                mobile_number=data['mobile_number'],
                state=data['state'],
                city=data['city'],
                address=data['address'],
                products_offered=data.get('products_offered'),
                products_needed=data.get('products_needed')
            )
            
            messages.success(request, f'Account created for {data["email"]}! You can now login.')
            return redirect('login')
    else:
        form = RegistrationForm() 
    return render(request, 'register.html', {'form': form})

def login_view(request):
    """
    Optional custom login view if you aren't using Django's built-in one.
    But in your sickle_project/urls.py you seem to use auth_views.LoginView.
    """
    pass

def marketplace_view(request):
    farmers = UserProfile.objects.filter(role__in=['farmer', 'both'])
    businesses = UserProfile.objects.filter(role__in=['business', 'both'])
    
    context = {
        'farmer_listings': farmers,
        'business_listings': businesses
    }
    return render(request, 'marketplace.html', context)

def product_list(request):
    products = Product.objects.filter(is_active=True).order_by("-created_at")
    return render(request, "product_list.html", {"products": products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk, is_active=True)
    return render(request, "product_detail.html", {"product": product})

@login_required
def product_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price_per_unit = request.POST.get('price_per_unit')
        quantity = request.POST.get('quantity')
        description = request.POST.get('description', '')
        
        Product.objects.create(
            farmer=request.user,
            name=name,
            price_per_unit=price_per_unit,
            available_quantity=quantity,
            description=description
        )
        messages.success(request, "Product listed successfully!")
        return redirect('dashboard')
        
    return render(request, "product_create.html")

@login_required
def order_create(request, product_pk):
    product = get_object_or_404(Product, pk=product_pk)
    if request.method == 'POST':
        quantity = float(request.POST.get('quantity', 0))
        if quantity > 0:
            Order.objects.create(
                product=product,
                buyer=request.user,
                quantity=quantity
            )
            messages.success(request, f"Order placed for {product.name}!")
            return redirect('dashboard')
    return render(request, "order_create.html", {"product": product})

@login_required
def dashboard(request):
    my_products = Product.objects.filter(farmer=request.user).order_by("-created_at")
    my_orders = Order.objects.filter(buyer=request.user).order_by("-created_at")
    return render(request, "dashboard.html", {"my_products": my_products, "my_orders": my_orders})