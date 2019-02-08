from django.urls import path

from . import views

app_name = 'billing'
urlpatterns = [
    path('payment-method/', views.payment_method_view, name='payment_method'),
    path('payment-method/create/', views.payment_method_create_view, name='payment_method_create'),
]
