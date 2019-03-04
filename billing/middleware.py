from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from billing.models import BillingProfile

class GuestSessionsMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        is_checkout = request.get_full_path() == reverse('shopcart:checkout')
        is_registering = request.get_full_path() == reverse('users:guest_register') 
        is_static = request.path.startswith(settings.STATIC_URL)
        # if app not billing, addresses, coupons or request path users/register
        checkout_keywords = ['billing', 'address', 'coupons', 'ship', 'edit']
        if any(word in request.get_full_path() for word in checkout_keywords):
            return response
        else:
            if not is_registering and not is_static:
                if 'guest_email_id' in request.session and is_checkout == False:
                    guest_email_id = request.session.get('guest_email_id')
                    if guest_email_id:
                        # get guest
                        # guest_obj = Guest.objects.get(id=guest_email_id)
                        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
                        # set inactive
                        billing_profile.set_inactive()
                        del request.session['guest_email_id']
                    if 'billing_address_id' in request.session:
                        del request.session['billing_address_id']
        return response