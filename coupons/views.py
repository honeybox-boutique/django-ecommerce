from django.shortcuts import render, redirect

from pricing.models import SDiscount
from .forms import SDiscountForm
from sales.models import Sale

def apply_discount_view(request):
    form = SDiscountForm(request.POST or None)# change: check if you're using this
    if form.is_valid():
        #get discount code from form
        discount_code = form.cleaned_data.get('sDiscountCouponCode')
        sale_id = form.cleaned_data.get('sobj')
        # billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
        # get sale from form hidden input
        sale_qs = Sale.objects.filter(saleStringID=sale_id,
                                    saleStatus='created',
                                    # saleBillingProfile=billing_profile,
                                )
        print('Sale Query Count')
        print(sale_qs.count())
        # get discount from coupon_code
        discount_qs = SDiscount.objects.filter(sDiscountCouponCode=discount_code,
                                    sDiscountIsActive=True,
                                )
        print('Discount Query Count')
        print(discount_qs.count())
        if sale_qs.count() == 1:
            sale_obj = sale_qs.first()
            if discount_qs.count() == 1:
                discount_obj = discount_qs.first()
                # check of sale meets discount conditions
                discount_conditions_met, reason, = sale_obj.check_discount_conditions(discount_obj)
                # if conditions met then apply discount (create many to many)
                if discount_conditions_met:
                    sale_obj.saleDiscounts.add(discount_obj)
                    print('added')
                else:
                    print(reason)
            else:
                print('no discount found')
        else:
            print('either multiple sale objects or none returned')
    else:
        print('invalid form submission')
    return redirect('shopcart:checkout')