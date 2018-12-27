from django.urls import path, include
from django.views.generic import ListView
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'products'
urlpatterns = [
    path('', views.ProductList.as_view(), name='list'),
    path('<int:pk>/detail/', views.ProductDetail.as_view(), name='detail'),
    path('<category>/', views.ProductList.as_view(), name='category'),
] 