from django.shortcuts import render

from .models import ShopCart
# Create your views here.
# from django.contrib.messages.views import SuccessMessageMixin
# 
# class ShopCartUpdateView(SuccessMessageMixin, UpdateView):
#     ...
#     success_message = 'List successfully saved!!!!'

def cart_home(request):
    cart_obj = ShopCart.objects.get_or_new(request)
    return render(request, 'carts/home.html', {})