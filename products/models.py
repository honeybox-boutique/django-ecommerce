import decimal
from django.db import models
from django.utils.text import slugify


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
    productSlug = models.SlugField(unique=True)
    productCategories = models.ManyToManyField(Category)

    #Calculated fields
    productDiscountAmount = models.DecimalField(null=True, max_digits=12, decimal_places=2)
    productSalePrice = models.DecimalField(null=True, max_digits=12, decimal_places=2)
    productBasePrice = models.DecimalField(null=True, max_digits=12, decimal_places=2)
    productDiscountType = models.CharField(null=True, max_length=40)
    productDiscountValue = models.DecimalField(null=True, max_digits=12, decimal_places=2)

    colorID = models.ManyToManyField(Color, through='ProductColor')

    class Meta:
        db_table = 'product'

    def __str__(self):
        return self.productName

    def get_absolute_url(self):
        return "/products/%s/%s" % (self.productCategories.first(), self.productSlug)
    

    def save(self, *args, **kwargs):
        if not self.productID:
            # Newly created object, so set slug
            self.productSlug = slugify(self.productName)

        super(Product, self).save(*args, **kwargs)

    #Calculate and return baseprice, discount amount, and saleprice for product
    def update_pricing(self):
        prod_base_price = decimal.Decimal("0.00")
        p_discount_type = None
        c_discount_type = None
        discount_type = None
        discount_value = decimal.Decimal("0.00")
        p_discount_amount = decimal.Decimal("0.00")
        c_discount_amount = decimal.Decimal("0.00")
        prod_discount_value = decimal.Decimal("0.00")
        cat_discount_value = decimal.Decimal("0.00")
        # get current base price
        pricing_obj = self.pricing_set.filter(pricingIsActive=True).first()# change: add error checking to pre_save on pricing and replace this with get()
        prod_base_price = pricing_obj.pricingBasePrice


        # get highest pdiscount_amount

        # get pdiscount_set
        prod_discount_obj = self.pdiscount_set.all()

        for discount in prod_discount_obj:
            p_discount_value, is_multiplier = discount.get_active_p_discount_amount_or_multiplier()

            # get the discount amount
            if is_multiplier:
                # calculate the things
                new_p_discount_amount = prod_base_price * p_discount_value

                if new_p_discount_amount > p_discount_amount:
                    p_discount_amount = new_p_discount_amount
                    p_discount_type = 'Percent'
                    prod_discount_value = p_discount_value
            else:
                new_p_discount_amount = p_discount_value

                # check if bigger than discount_amount

                if new_p_discount_amount > p_discount_amount:
                    # assign to p_discount_amount
                    p_discount_amount = new_p_discount_amount
                    p_discount_type = 'Decimal'
                    prod_discount_value = p_discount_value

        # get highest cdiscount_amount in categories

        category_query = self.productCategories
        for category in category_query.all():
            # get cdiscount_set.all
            category_discounts_set = category.cdiscount_set.all()
            for discount in category_discounts_set:
                # discount.get_cdiscount_amount_or_multiplier
                c_discount_value, is_multiplier = discount.get_active_cdiscount_amount_or_multiplier()

                # get the discount amount
                if is_multiplier:
                    # calculate the things
                    new_c_discount_amount = prod_base_price * c_discount_value

                    if new_c_discount_amount > c_discount_amount:
                        c_discount_amount = new_c_discount_amount
                        c_discount_type = 'Percent'
                        cat_discount_value = c_discount_value
                else:
                    new_c_discount_amount = c_discount_value

                    # check if bigger than discount_amount

                    if new_c_discount_amount > c_discount_amount:
                        # assign to c_discount_amount
                        c_discount_amount = new_c_discount_amount
                        c_discount_type = 'Decimal'
                        cat_discount_value = c_discount_value

        # set bigger amount to self.productDiscountAmount
        if p_discount_amount > c_discount_amount:
            product_discount_amount = p_discount_amount
            discount_type = p_discount_type
            discount_value = prod_discount_value
        else:
            product_discount_amount = c_discount_amount
            discount_type = c_discount_type
            discount_value = cat_discount_value
        
        # set product_sale_price variable
        product_sale_price = prod_base_price - product_discount_amount

        print(self.productName)
        print('Base Price')
        print(prod_base_price)
        print('Discount Type')
        print(discount_type)
        print('Discount Value')
        print(discount_value)
        print('Discount')
        print(product_discount_amount)
        print('Sale Price')
        print(product_sale_price)
        self.productBasePrice = prod_base_price
        self.productDiscountType = discount_type
        self.productDiscountValue = discount_value
        self.productDiscountAmount = product_discount_amount
        self.productSalePrice = product_sale_price
        self.save()
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
