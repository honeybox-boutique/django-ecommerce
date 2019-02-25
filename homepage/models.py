from django.db import models

# Create your models here.


class HomePageImage(models.Model):
    homePageImageID = models.AutoField(primary_key=True)
    homePageImagePath = models.ImageField(upload_to='homepage')
    homePageImageAltText = models.CharField(max_length=120)
    homePageImageLink = models.URLField()


    class Meta:
        db_table = 'home_page_image'

class BigHomePageImage(models.Model):
    bigHomePageImageID = models.AutoField(primary_key=True)
    bigHomePageImagePath = models.ImageField(upload_to='homepage')
    bigHomePageImageAltText = models.CharField(max_length=120)
    bigHomePageImageLink = models.URLField()


    class Meta:
        db_table = 'big_home_page_image'