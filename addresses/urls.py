from django.urls import path, include
from django.views.generic import TemplateView

from .views import checkout_address_create_view, checkout_address_reuse_view

app_name = 'addresses'
urlpatterns = [
    path('checkout/create/', checkout_address_create_view, name='checkout_address_create'),
    path('checkout/reuse/', checkout_address_reuse_view, name='checkout_address_reuse'),
]