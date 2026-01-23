from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("smpt/", views.product_list, name="product_list"),  # SMPT marketplace
    path("smpt/<int:pk>/", views.product_detail, name="product_detail"),
    path("smpt/<int:product_pk>/order/", views.order_create, name="order_create"),
    path("products/new/", views.product_create, name="product_create"),
    path("dashboard/", views.dashboard, name="dashboard"),
]