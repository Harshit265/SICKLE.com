from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('profession/', views.select_profession, name='select_profession'),
    path('marketplace/', views.marketplace, name='marketplace'),
] # Make sure there is only one closing bracket here