# FILE: store/urls.py (Your app's URL file)

from django.contrib import admin
from django.urls import path
from store import views

urlpatterns = [
    # Main pages
    path('', views.home, name='homepage'),
    path('product-detail/<int:pk>', views.productdetail, name='product-detail'),

    # Auth
    path('signup', views.signup.as_view(), name='signup'),
    path('login', views.Login.as_view(), name='login'),
    path('logout', views.logout, name='logout'),

    # Cart functions
    path('add_to_cart', views.add_to_cart, name='add_to_cart'),
    path('show_cart', views.show_cart, name='show-cart'),
    path('plus_cart', views.plus_cart, name='plus-cart'),
    path('minus_cart', views.minus_cart, name='minus-cart'),
    path('remove_cart', views.remove_cart, name='remove-cart'),

    # Orders and Payment Flow (Using views.checkout correctly)
    path('checkout', views.checkout, name='checkout'),
    path('initiate_otp', views.initiate_otp, name='initiate_otp'),
    path('verify_otp', views.verify_otp_view, name='verify_otp'),

    path('orders', views.orders_view, name='orders'),
    path('order_success', views.order_success_view, name='order_success'),


]