from django.urls import path, include

from . import views

app_name = 'coupons'
urlpatterns = [
    path('apply-discount/', views.apply_discount_view, name='apply_discount'),
]
