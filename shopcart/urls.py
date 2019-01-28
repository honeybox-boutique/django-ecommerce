from django.urls import path, include
from . import views

app_name = 'shopcart'
urlpatterns = [
    path('home/', views.cart_home, name='cart_home'),
]
