from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.


class Vendor(models.Model):   
    vendorID = models.AutoField(primary_key=True)
    vendorName = models.CharField(max_length=200)
    vendorDescription = models.CharField(max_length=200)
    vendorNotes = models.CharField(max_length=200)
    vendorWebsite = models.CharField(max_length=200)

    class Meta:
            db_table = 'vendor'

    def __str__(self):
        return self.vendorName

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

    productCategories = models.ManyToManyField(Category)

    class Meta:
            db_table = 'product'

    def __str__(self):
        return self.productName


class ProductImage(models.Model):   
    productImageID = models.AutoField(primary_key=True)
    productImagePath = models.ImageField(upload_to='products')

    productID = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
            db_table = 'product_image'


class TransactionType(models.Model):   
    transactionTypeID = models.AutoField(primary_key=True)
    transactionTypeName = models.CharField(max_length=200)
    transactionTypeDescription = models.CharField(max_length=200)

    class Meta:
            db_table = 'transaction_type'

    def __str__(self):
        return self.transactionTypeName

class Transaction(models.Model):
    transactionID = models.AutoField(primary_key=True)
    transactionDate = models.DateTimeField('date purchased')
    transactionNote = models.CharField(max_length=200)
    transactionStatus = models.CharField(max_length=200)

    productID = models.ManyToManyField(Product, through='PurchaseItems')
    transactionTypeID = models.ForeignKey(TransactionType, on_delete=models.CASCADE)
    userID = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
            db_table = 'transaction'

    def __str__(self):
        return self.transactionID

class PurchaseItems(models.Model):   
    prodStockID = models.AutoField(primary_key=True)
    piPrice = models.DecimalField(max_digits=8, decimal_places=3)
    piSize = models.CharField(max_length=200)
    piColor = models.CharField(max_length=200)
    piCondition = models.CharField(max_length=200)
    piNotes = models.CharField(max_length=200)
    piBarcode = models.ImageField(upload_to='barcodes')
    

    transactionID = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    productID = models.ForeignKey(Product, on_delete=models.CASCADE)
    vendorID = models.ForeignKey(Vendor, on_delete=models.CASCADE)

    class Meta:
            db_table = 'purchase_items'

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

