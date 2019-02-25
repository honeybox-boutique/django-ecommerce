from django.contrib import admin

from .models import HomePageImage, BigHomePageImage

admin.site.register(BigHomePageImage)
admin.site.register(HomePageImage)