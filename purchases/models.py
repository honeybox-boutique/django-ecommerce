from django.db import models
from django.conf import settings
from products.models import Product, Color, ProductImage

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

class Purchase(models.Model):
    purchaseID = models.AutoField(primary_key=True)
    purchaseDate = models.DateTimeField('date purchased')
    purchaseNote = models.TextField(max_length=200)
    purchaseStatus = models.CharField(max_length=40)

    productID = models.ManyToManyField(Product, through='PurchaseItems')
    userID = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        db_table = 'purchase'

    def __str__(self):
        return self.purchaseNote

class PurchaseItems(models.Model):
    prodStockID = models.AutoField(primary_key=True)
    piPrice = models.DecimalField(max_digits=8, decimal_places=3)
    piSize = models.CharField(max_length=20)
    piCondition = models.CharField(max_length=50)
    piNotes = models.TextField(max_length=200)
    piBarcode = models.ImageField(upload_to='barcodes', blank=True, null=True)

    piColor = models.ForeignKey(Color, on_delete=models.CASCADE)
    purchaseID = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    productID = models.ForeignKey(Product, on_delete=models.CASCADE)
    vendorID = models.ForeignKey(Vendor, on_delete=models.CASCADE)

    # field to determine if item is available for sale
    piIsAvailable = models.BooleanField(default=True)

    class Meta:
        db_table = 'purchase_items'

    def __str__(self):
        return str(self.productID)
    
    def get_image_set(self):
        ''' gets product color image set for prodstock '''
        item_color = self.piColor
        # get images
        item_images = ProductImage.objects.filter(
            # item_color
            productColorID__colorID=item_color,
            # product_id
            productColorID__productID=self.productID
        )
        print(item_images.first())
        return item_images