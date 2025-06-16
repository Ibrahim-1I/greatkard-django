from django.urls import path
from . import views  # Import your views module

urlpatterns = [
   path('register/', views.register, name='register'),  # Reference the 'cart' view from views
   path('login/', views.login, name='login'),  # Reference the 'cart' view from views
    path('logout/', views.logout, name='logout'),  # Reference the 'cart' view from views
    path('dashboard/', views.dashboard, name='dashboard'),  # Reference the 'cart' view from views
    path('', views.dashboard, name='dashboard'),  # Default dashboard view
    path('forgotPassword/', views.forgotPassword, name='forgotPassword'),  # Reference the 'cart' view from views



    path('activate/<uidb64>/<token>/', views.activate, name='activate'),  # Reference the 'cart' view from views
    path('resetpassword_validate/<uidb64>/<token>/', views.resetpassword_validate, name='resetpassword_validate'),  # Reference the 'cart' view from views
    path('resetPassword/', views.resetPassword, name='resetPassword'),  # Reference the 'cart' view from views


   
]    