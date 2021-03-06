"""speedtest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from emails.views import send_email_view, email_success_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('products/', include('products.urls')),
    path('purchases/', include('purchases.urls')),
    path('shopcart/', include('shopcart.urls')),
    path('pricing/', include('pricing.urls')),
    path('billing/', include('billing.urls')),
    path('sales/', include('sales.urls')),
    path('address/', include('addresses.urls')),
    path('coupons/', include('coupons.urls')),
    path('', include('homepage.urls')),
    path('returns/', TemplateView.as_view(template_name="returns.html"), name='returns'),
    path('shipping/', TemplateView.as_view(template_name="shipping.html"), name='shipping'),
    path('data-privacy/', TemplateView.as_view(template_name="data-privacy.html"), name='dataprivacy'),
    path('terms-of-service/', TemplateView.as_view(template_name="terms-of-service.html"), name='tos'),
    path('contact-us/', send_email_view, name='contact'),
    path('contact-us/thanks/', email_success_view, name='contact_thanks'),
    path('coming-soon/', TemplateView.as_view(template_name="coming-soon.html"), name='coming-soon'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),

        # For django versions before 2.0:
        # url(r'^__debug__/', include(debug_toolbar.urls)),

    ] + urlpatterns
