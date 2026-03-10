from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from marketplace import views as marketplace_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', marketplace_views.home, name='home'),
    path('register/', marketplace_views.register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('marketplace/', marketplace_views.marketplace_view, name='marketplace'),
    path('', include('marketplace.urls')),
]
