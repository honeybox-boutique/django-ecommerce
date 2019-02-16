from django.urls import path, include, reverse_lazy
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views

from . import views

app_name = 'users'
urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('password_reset/', auth_views.PasswordResetView.as_view(success_url=reverse_lazy('users:password_reset_confirm')), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('guest/register/', views.guest_register_view, name='guest_register'),
    path('signup/next<path:next>', views.SignUpView.as_view(), name='signup'),
]