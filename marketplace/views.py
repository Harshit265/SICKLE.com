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
                gst_number=data.get('gst_number', '')
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

from django.db.models import Q

def marketplace_view(request):
    query = request.GET.get('search', '')
    farmers = UserProfile.objects.filter(role__in=['farmer', 'both'])
    businesses = UserProfile.objects.filter(role__in=['business', 'both'])
    
    if query:
        farmers = farmers.filter(Q(full_name__icontains=query) | Q(city__icontains=query) | Q(state__icontains=query))
        businesses = businesses.filter(Q(full_name__icontains=query) | Q(city__icontains=query) | Q(state__icontains=query))
    
    context = {
        'farmer_listings': farmers,
        'business_listings': businesses,
        'search_query': query
    }
    return render(request, 'marketplace.html', context)

def product_list(request):
    query = request.GET.get('search', '')
    products = Product.objects.filter(is_active=True).order_by("-created_at")
    if query:
        products = products.filter(name__icontains=query)
    return render(request, "product_list.html", {"products": products, "search_query": query})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk, is_active=True)
    return render(request, "product_detail.html", {"product": product})

@login_required
def product_create(request):
    from .models import Category, HSNCode
    if request.method == 'POST':
        name = request.POST.get('name')
        price_per_unit = request.POST.get('price_per_unit')
        quantity = request.POST.get('quantity')
        description = request.POST.get('description', '')
        category_id = request.POST.get('category')
        hsn_id = request.POST.get('hsn_code')
        
        category = Category.objects.filter(id=category_id).first() if category_id else None
        hsn_code = HSNCode.objects.filter(id=hsn_id).first() if hsn_id else None
        
        Product.objects.create(
            farmer=request.user,
            name=name,
            price_per_unit=price_per_unit,
            available_quantity=quantity,
            description=description,
            category=category,
            hsn_code=hsn_code
        )
        messages.success(request, "Product listed successfully!")
        return redirect('dashboard')
        
    categories = Category.objects.all()
    hsn_codes = HSNCode.objects.all()
    return render(request, "product_create.html", {"categories": categories, "hsn_codes": hsn_codes})

@login_required
def order_create(request, product_pk):
    product = get_object_or_404(Product, pk=product_pk)
    
    total_tax_rate = 0
    if product.hsn_code:
        # Simplification: use IGST for total max rate preview or sum of CGST+SGST
        total_tax_rate = product.hsn_code.igst_rate if product.hsn_code.igst_rate > 0 else (product.hsn_code.cgst_rate + product.hsn_code.sgst_rate)

    if request.method == 'POST':
        quantity = float(request.POST.get('quantity', 0))
        if quantity > 0:
            buyer_state = request.user.userprofile.state.lower().strip() if request.user.userprofile.state else ""
            farmer_state = product.farmer.userprofile.state.lower().strip() if product.farmer.userprofile.state else ""
            
            sub_total = float(quantity) * float(product.price_per_unit)
            
            cgst_amount = 0
            sgst_amount = 0
            igst_amount = 0
            tax_rate_applied = 0
            tax_type = ""
            
            if product.hsn_code:
                if buyer_state == farmer_state and buyer_state != "":
                    # Intra-state
                    tax_type = "CGST+SGST"
                    cgst_rate = float(product.hsn_code.cgst_rate)
                    sgst_rate = float(product.hsn_code.sgst_rate)
                    cgst_amount = sub_total * (cgst_rate / 100)
                    sgst_amount = sub_total * (sgst_rate / 100)
                    tax_rate_applied = cgst_rate + sgst_rate
                else:
                    # Inter-state or missing state info
                    tax_type = "IGST"
                    igst_rate = float(product.hsn_code.igst_rate)
                    igst_amount = sub_total * (igst_rate / 100)
                    tax_rate_applied = igst_rate

            grand_total = sub_total + cgst_amount + sgst_amount + igst_amount

            order = Order.objects.create(
                product=product,
                buyer=request.user,
                quantity=quantity,
                sub_total=sub_total,
                cgst_amount=cgst_amount,
                sgst_amount=sgst_amount,
                igst_amount=igst_amount,
                grand_total=grand_total,
                tax_rate_applied=tax_rate_applied,
                tax_type=tax_type
            )
            messages.success(request, f"Order placed for {product.name}!")
            return redirect('order_bill', pk=order.pk)
    return render(request, "order_create.html", {"product": product, "total_tax_rate": total_tax_rate})

@login_required
def order_bill(request, pk):
    order = get_object_or_404(Order, pk=pk, buyer=request.user)
    return render(request, "order_bill.html", {"order": order})

@login_required
def dashboard(request):
    query = request.GET.get('search', '')
    my_products = Product.objects.filter(farmer=request.user).order_by("-created_at")
    my_orders = Order.objects.filter(buyer=request.user).order_by("-created_at")
    
    if query:
        my_products = my_products.filter(name__icontains=query)
        my_orders = my_orders.filter(product__name__icontains=query)

    return render(request, "dashboard.html", {
        "my_products": my_products, 
        "my_orders": my_orders,
        "search_query": query
    })

def profile_view(request, pk):
    target_user = get_object_or_404(User, pk=pk)
    target_profile = get_object_or_404(UserProfile, user=target_user)
    
    # Products offered by this user
    user_products = Product.objects.filter(farmer=target_user, is_active=True).order_by("-created_at")
    
    context = {
        'profile': target_profile,
        'user_products': user_products
    }
    return render(request, 'profile.html', context)