from django.urls import path, include
from django.views.generic import TemplateView

from . import views

app_name = 'addresses'
urlpatterns = [
    path('checkout/create/', views.checkout_address_create_view, name='checkout_address_create'),
    path('checkout/reuse/', views.checkout_address_reuse_view, name='checkout_address_reuse'),
]