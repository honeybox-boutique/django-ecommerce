from django.urls import path, reverse_lazy
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views

from .views import guest_register_view, SignUpView, dashboard, PasswordResetView

app_name = 'users'
urlpatterns = [
    path('guest/register/', guest_register_view, name='guest_register'),
    path('signup/next<path:next>', SignUpView.as_view(), name='signup'),
    # path('', include('django.contrib.auth.urls')),
     # url(r'signup/$', signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # url(r'password_change/$',auth_views.PasswordChangeView.as_view(template_name='password_change.html',success_url='/accounts/password_change_done')),
    # url(r'password_change_done/',auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html')),
    # url(r'password_reset/$',auth_views.PasswordResetView.as_view(template_name='password_reset.html',email_template_name='password_reset_email.html',subject_template_name='password_reset_subject.txt',success_url='/accounts/password_reset_done/',from_email='support@yoursite.ma')),
    # url(r'password_reset_done/',auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html')),
    # url(r'password_reset_confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html',success_url='/accounts/password_reset_complete/')),
    # url(r'password_reset_complete/',auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html')),
    path('password_reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('password_reset/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(success_url=reverse_lazy('users:password_reset_complete')), name='password_reset_confirm'),
    path('password_reset/', PasswordResetView.as_view(email_template_name='registration/password_reset_email.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('dashboard/', dashboard, name='dashboard'),
]