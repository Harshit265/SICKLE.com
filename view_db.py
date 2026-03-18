import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sickle_project.settings')
django.setup()

from django.contrib.auth.models import User
from marketplace.models import UserProfile, Product, Order

print("=== DATABASE CONTENTS ===\n")

print("--- USERS ---")
users = User.objects.all()
if not users:
    print("No users found.")
for u in users:
    print(f"ID: {u.id} | Username: {u.username} | Email: {u.email}")

print("\n--- USER PROFILES ---")
profiles = UserProfile.objects.all()
if not profiles:
    print("No profiles found.")
for p in profiles:
    print(f"User: {p.user.username} | Name: {p.full_name} | Role: {p.role} | Location: {p.city}, {p.state}")

print("\n--- PRODUCTS ---")
products = Product.objects.all()
if not products:
    print("No products listed.")
for p in products:
    print(f"Farmer: {p.farmer.username} | Product: {p.name} | Price: ₹{p.price_per_unit}/{p.unit} | Stock: {p.available_quantity}")

print("\n--- ORDERS ---")
orders = Order.objects.all()
if not orders:
    print("No orders placed.")
for o in orders:
    print(f"Buyer: {o.buyer.username} | Product: {o.product.name} | Qty: {o.quantity} | Total: ₹{o.total_price} | Status: {o.status}")

print("\n=========================")
