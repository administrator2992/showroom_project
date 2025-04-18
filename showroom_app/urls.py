from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.mobil_list, name='mobil_list'),
    path('mobil/new/', views.mobil_create, name='mobil_create'),
    path('mobil/<int:pk>/', views.mobil_detail, name='mobil_detail'),
    path('mobil/<int:pk>/edit/', views.mobil_update, name='mobil_update'),
    path('mobil/<int:pk>/delete/', views.mobil_delete, name='mobil_delete'),
    path('mobil/<int:mobil_pk>/service/new/', views.service_create, name='service_create'),
    path('accounts/login/', views.user_login, name='login'),
    path('accounts/logout/', views.MessageLogoutView.as_view(), name='logout'),
    path('change-password/', views.change_password, name='change_password'),
    path('register/', views.register, name='register'),
]
