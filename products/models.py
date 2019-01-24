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

    productColorID = models.ForeignKey(ProductColor, on_delete=models.CASCADE)

    class Meta:
        db_table = 'product_image'
