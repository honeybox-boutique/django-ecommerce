from django.db import models

# Create your models here.

# class Brand(models.Model):
    # brand_name = models.CharField(max_length=50)

class Category(models.Model):   
    category_name = models.CharField(max_length=200)
    category_description = models.CharField(max_length=200)

    def __str__(self):
        return self.category_name

class CategoryImage(models.Model):
    cat_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    cat_image = models.ImageField(upload_to='categories')

class Product(models.Model):
    prod_name = models.CharField(max_length=200)
    prod_description = models.CharField(max_length=200)
    prod_price = models.DecimalField(max_digits=8, decimal_places=2) 
    prod_color = models.CharField(max_length=30)
    prod_categories = models.ManyToManyField(Category)
    # brand_id = models.ForeignKey(Brand, on_delete=models.CASCADE)

    def __str__(self):
        return self.prod_name


class ProductImage(models.Model):   
    prod_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    prod_image = models.ImageField(upload_to='products')


# class ProdCategory(models.Model):   

# class ProductImage(models.Model):   # Image uploading / storage needs to be configured still. See model field reference in django docs for details
    # prod_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    # prod_image = models.CharField(max_length=200)
    # prod_price = models.DecimalField(max_digits=8, decimal_places=2)
    # prod_date_purchased = models.DateTimeField('date purchased')

# class Size(models.Model):
    # size_name = models.CharField(max_length=200)
    # prod_description = models.CharField(max_length=200)
    # prod_price = models.DecimalField(max_digits=8, decimal_places=2)

# class ProdSize(models.Model):

# class Color(models.Model):
    # color_name = models.CharField(max_length=200)
    # prod_description = models.CharField(max_length=200)
    # prod_price = models.DecimalField(max_digits=8, decimal_places=2)

# class ProdColor(models.Model):



# class Purchase(models.Model):
    # prod_name = models.CharField(max_length=200)
    # prod_description = models.CharField(max_length=200)
    # prod_price = models.DecimalField(max_digits=8, decimal_places=2) 
    # prod_date_purchased = models.DateTimeField('date purchased')
    # prod_date_available = models.DateTimeField('date available')

# class Sale(models.Model):
    # prod_name = models.CharField(max_length=200)
    # prod_description = models.CharField(max_length=200)
    # prod_price = models.DecimalField(max_digits=8, decimal_places=2) 
    # prod_date_purchased = models.DateTimeField('date purchased')
    # prod_date_available = models.DateTimeField('date available')

# class Vendor(models.Model):
    # vendor_name = models.CharField(max_length=200)
    # vendor_url = models.CharField(max_length=200)
    # vendor_notes = models.CharField(max_length=200)

