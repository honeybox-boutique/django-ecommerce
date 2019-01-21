from django import template
from ..forms import ProductSizeColorForm
register = template.Library()

# def __init__(self, obj):
    # from django.template import Variable
    # // get the variable value
    # self.id = Variable(obj)
@register.simple_tag(takes_context=True)
def get_discount_price(context, price):
    if context['product'].pricing_set.first().productID.pdiscount_set.first().pDiscountType == 'Percent':
        discount_amount = price - (price * context['product'].pricing_set.first().productID.pdiscount_set.first().pDiscountValue)
        context['price'] = discount_amount
        return discount_amount
    elif context['product'].pricing_set.first().productID.pdiscount_set.first().pDiscountType == 'Amount':
        discount_amount = price - context['product'].pricing_set.first().productID.pdiscount_set.first().pDiscountValue
        context['price'] = discount_amount
        return discount_amount

@register.inclusion_tag('products/_form.html', takes_context=True)
def product_size_color_form(context):
    form = ProductSizeColorForm()
    context['form'] = form
    return {'form': form}
# def get_discount_price(self, price):
    # if self.pDiscountType == 'Percent':
        # discount_amount = price - (price * self.pDiscountValue)
        # return discount_amount
    # elif self.pDiscountType == 'Amount':
        # discount_amount = price - self.pDiscountValue
        # return discount_amount