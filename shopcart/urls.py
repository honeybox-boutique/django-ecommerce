from django.urls import path, include

from . import views

app_name = 'shopcart'
urlpatterns = [
    path('home/', views.cart_home, name='home'),
    path('update/', views.cart_update, name='update'),
    path('checkout/', views.checkout_home, name='checkout'),
]
