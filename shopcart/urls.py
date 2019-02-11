from django.urls import path, include

from . import views

app_name = 'shopcart'
urlpatterns = [
    path('home/', views.cart_home, name='home'),
    path('update/', views.cart_update, name='update'),
    path('remove/', views.cart_remove_item, name='remove'),
    path('edit-shipping/', views.edit_shipping, name='edit_shipping'),
    path('edit-billing/', views.edit_billing, name='edit_billing'),
    path('ship-method/', views.ship_method, name='ship_method'),
    path('checkout/success/', views.checkout_done_view, name='success'),
    path('checkout/', views.checkout_home, name='checkout'),
]
