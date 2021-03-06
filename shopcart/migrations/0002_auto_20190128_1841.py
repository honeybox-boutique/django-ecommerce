# Generated by Django 2.1.4 on 2019-01-28 18:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('purchases', '0002_auto_20190125_0050'),
        ('shopcart', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShopCart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shopCartDateCreated', models.DateTimeField(auto_now_add=True)),
                ('shopCartLastModified', models.DateTimeField(auto_now=True)),
                ('shopCartStatus', models.CharField(choices=[('Open', 'Open - currently active'), ('Saved', 'Saved - for items to be purchased later'), ('Frozen', 'Frozen - the basket cannot be modified'), ('Submitted', 'Submitted - has been ordered at the checkout')], default='Open', max_length=40)),
                ('shopCartDiscount', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('shopCartSubTotal', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('shopCartItems', models.ManyToManyField(blank=True, to='purchases.PurchaseItems')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'shopcart',
            },
        ),
        migrations.DeleteModel(
            name='ShoppingCart',
        ),
    ]
