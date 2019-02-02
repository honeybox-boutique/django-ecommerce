from django.db import models
from django.utils.text import slugify

# Create your models here.
# Add color table
class Color(models.Model):
    colorID = models.AutoField(primary_key=True)
    colorName = models.CharField(max_length=50)
    colorDescription = models.TextField(max_length=200)

    class Meta:
        db_table = 'color'

    def __str__(self):
        return self.colorName
# Add/modify productImageTable

class Category(models.Model):
    categoryName = models.CharField(max_length=200)
    categoryDescription = models.CharField(max_length=200)

    class Meta:
        db_table = 'category'

    def __str__(self):
        return self.categoryName

class CategoryImage(models.Model):
    categoryImageID = models.AutoField(primary_key=True)
    categoryImagePath = models.ImageField(upload_to='categories')

    categoryID = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        db_table = 'category_image'

class Product(models.Model):
    productID = models.AutoField(primary_key=True)
    productName = models.CharField(max_length=200)
    productDescription = models.CharField(max_length=200)
    productSlug = models.SlugField(unique=False)
    productCategories = models.ManyToManyField(Category)

    colorID = models.ManyToManyField(Color, through='ProductColor')

    class Meta:
        db_table = 'product'

    def __str__(self):
        return self.productName

    def save(self, *args, **kwargs):
        if not self.productID:
            # Newly created object, so set slug
            self.productSlug = slugify(self.productName)

        super(Product, self).save(*args, **kwargs)

    #Calculate and return baseprice, discount amount, and saleprice for product
    # def get_pricing(self, request):
    
        # get product base price
        # pricing_obj = self.pricing_set.filter(pricingIsActive=True).first()# change: add error checking to pre_save on pricing and replace this with get()
        # prod_discount_obj = self.pdiscount_set.filter()
        # category_query = self.productCategories
        # c_discount_value, is_multiplier = self.productCategories.cdiscount_set

        # get highest pdiscount_amount

        # get highest cdiscount_amount in categories

        # c_discount_amount = 0
        # for category in category_query
            # get cdiscount_set.all
            # for discount in cdiscount_set.all
                # discount.get_cdiscount_amount_or_multiplier

                # get the discount amount
                # if multiplier:
                    # calculate the things
                    # new_c_discount_amount = (base price * discount_value)

                    # if new_c_discount_amount > c_discount_amount:
                        # c_discount_amount = new_c_discount_amount
                # else:
                    # new_c_discount_amount = discount_value
                    # return new_c_discount_amount

                    # check if bigger than discount_amount

                    # if new_c_discount_amount > c_discount_amount:
                        # assign to c_discount_amount
                        # c_discount_amount = new_c_discount_amount

        # return pricing_obj

# Add many to many through purchitemcolor table
class ProductColor(models.Model):
    productColorID = models.AutoField(primary_key=True)
    productColorName = models.CharField(max_length=40)

    productID = models.ForeignKey(Product, on_delete=models.CASCADE)
    colorID = models.ForeignKey(Color, on_delete=models.CASCADE)

    class Meta:
        db_table = 'product_color_set'

    def __str__(self):
        return self.productColorName

class ProductImage(models.Model):
    productImageID = models.AutoField(primary_key=True)
    productImagePath = models.ImageField(upload_to='products')
    # Add alt text field here - productImageAltText = models.CharField(max_length=40)

    productColorID = models.ForeignKey(ProductColor, on_delete=models.CASCADE)

    class Meta:
        db_table = 'product_image'
