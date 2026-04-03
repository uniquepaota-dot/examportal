from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('password-change/', views.admin_change_password_view, name='admin_password_change'),
    path('dashboard/', views.dashboard_redirect, name='dashboard'),
]
