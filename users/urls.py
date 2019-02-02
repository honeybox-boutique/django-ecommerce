from django.urls import path, include
from django.views.generic import TemplateView

from . import views

app_name = 'users'
urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('signup/next<path:next>', views.SignUpView.as_view(), name='signup'),
]