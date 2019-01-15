from django.db import models
from django.conf import settings
from products.models import Product

# Create your models here.

class Vendor(models.Model):
    vendorID = models.AutoField(primary_key=True)
    vendorName = models.CharField(max_length=40)
    vendorDescription = models.TextField(max_length=200)
    vendorNotes = models.TextField(max_length=200)
    vendorWebsite = models.URLField(max_length=200)

    class Meta:
        db_table = 'vendor'

    def __str__(self):
        return self.vendorName

class TransactionType(models.Model):
    transactionTypeID = models.AutoField(primary_key=True)
    transactionTypeName = models.CharField(max_length=40)
    transactionTypeDescription = models.TextField(max_length=200)

    class Meta:
        db_table = 'transaction_type'

    def __str__(self):
        return self.transactionTypeName

class Transaction(models.Model):
    transactionID = models.AutoField(primary_key=True)
    transactionDate = models.DateTimeField('date purchased')
    transactionNote = models.TextField(max_length=200)
    transactionStatus = models.CharField(max_length=40)

    productID = models.ManyToManyField(Product, through='PurchaseItems')
    transactionTypeID = models.ForeignKey(TransactionType, on_delete=models.CASCADE)
    userID = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        db_table = 'transaction'

    def __str__(self):
        return self.transactionNote

class PurchaseItems(models.Model):
    prodStockID = models.AutoField(primary_key=True)
    piPrice = models.DecimalField(max_digits=8, decimal_places=3)
    piSize = models.CharField(max_length=20)
    piColor = models.CharField(max_length=40)
    piCondition = models.CharField(max_length=50)
    piNotes = models.TextField(max_length=200)
    piBarcode = models.ImageField(upload_to='barcodes')

    transactionID = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    productID = models.ForeignKey(Product, on_delete=models.CASCADE)
    vendorID = models.ForeignKey(Vendor, on_delete=models.CASCADE)

    class Meta:
        db_table = 'purchase_items'
