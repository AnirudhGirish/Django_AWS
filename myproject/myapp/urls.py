from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('app/', views.app_view, name='app'),
    path('credentials/', views.credentials_view, name='credentials'),
    path('delete_credential/<int:cred_id>/', views.delete_credential, name='delete_credential'),
    path('profile/', views.profile_view, name='profile'),
]