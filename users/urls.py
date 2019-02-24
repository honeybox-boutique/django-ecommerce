from django.urls import path, reverse_lazy, re_path
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views

from .views import guest_register_view, SignUpView, PasswordResetView, dashboard, dashboard_addresses, dashboard_payment_methods, dashboard_orders, DashboardOrderListView, DashboardOrderDetailView, DashboardCardListView

app_name = 'users'
urlpatterns = [
    path('guest/register/', guest_register_view, name='guest_register'),
    path('signup/next<path:next>', SignUpView.as_view(), name='signup'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('password_reset/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(success_url=reverse_lazy('users:password_reset_complete')), name='password_reset_confirm'),
    path('password_reset/', PasswordResetView.as_view(email_template_name='registration/password_reset_email.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('dashboard/', dashboard, name='dashboard'),
    path('dashboard/addresses/', dashboard_addresses, name='dashboard_addresses'),
    path('dashboard/payment-methods/', dashboard_payment_methods, name='dashboard_payment_methods'),
    path('dashboard/orders/', DashboardOrderListView.as_view(), name='dashboard_orders'),
    path('dashboard/orders/<pk>', DashboardOrderDetailView.as_view(), name='dashboard_order_detail'),
]