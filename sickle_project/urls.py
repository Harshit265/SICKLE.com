from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from marketplace import views as marketplace_views # Replace 'marketplace' with your app name



urlpatterns = [
    path('', marketplace_views.home, name='home'),
    path('register/', marketplace_views.register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('admin/', admin.site.urls),
]
