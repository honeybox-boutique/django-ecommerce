from django.db import models

# Create your models here.

class ShoppingCart(models.Model):
    shoppingCartID = models.AutoField(primary_key=True)
    vendorName = models.CharField(max_length=40)
    vendorDescription = models.TextField(max_length=200)
    vendorNotes = models.TextField(max_length=200)
    vendorWebsite = models.URLField(max_length=200)

    class Meta:
        db_table = 'shopping_cart'

# class Cart(models.Model):
    # user = models.ForeignKey(User, null = True, blank = True)
    # products = models.ManyToManyField(Product, blank= True)

    # subtotal = models.DecimalField(default = 0.00, max_digits= 12, decimal_places=2)

    # total = models.DecimalField(default = 0.00, max_digits= 12, decimal_places=2)
    # updated = models.DateTimeField(auto_now =True)
    # timestamp = models.DateTimeField(auto_now_add  = True)
    # objects  = CartManager()

    # def __str__(self):
        # return str(self.id)

# class CartManager(models.Manager):
    # def get_or_new(self,request):
        # cart_id = request.session.get('cart_id', None)
        # qs = self.get_queryset().filter(id = cart_id)
        # if qs.count() ==1:
            # new_obj = False
            # cart_obj = qs.first()
            # if request.user.is_authenticated() and cart_obj.user is None:
                # cart_obj.user = request.user
                # cart_obj.save()
       # else:
            # new_obj = True
            # cart_obj = Cart.objects.new_cart(user = request.user)
            # request.session['cart_id'] = cart_obj.id
       # return cart_obj, new_obj