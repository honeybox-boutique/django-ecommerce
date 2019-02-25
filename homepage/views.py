from django.shortcuts import render
from django.views.generic import TemplateView

from .models import HomePageImage, BigHomePageImage
# Create your views here.
class HomePageTemplateView(TemplateView):
   template_name = 'index.html'

   def get_context_data(self, **kwargs):
       context = super(HomePageTemplateView, self).get_context_data(**kwargs)

       context['big_image_qs'] = BigHomePageImage.objects.all()
       context['image_qs'] = HomePageImage.objects.all()
       return context