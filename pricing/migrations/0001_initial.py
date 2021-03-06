# Generated by Django 2.1.4 on 2019-01-21 16:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CDiscount',
            fields=[
                ('cDiscountID', models.AutoField(primary_key=True, serialize=False)),
                ('cDiscountName', models.CharField(max_length=40)),
                ('cDiscountDescription', models.TextField(max_length=200)),
                ('cDiscountType', models.CharField(max_length=30)),
                ('cDiscountValue', models.DecimalField(decimal_places=3, max_digits=8)),
                ('cDiscountDateCreated', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('cDiscountDateValidFrom', models.DateTimeField(verbose_name='valid from')),
                ('cDiscountDateValidUntil', models.DateTimeField(verbose_name='valid until')),
                ('cDiscountCouponCode', models.CharField(max_length=20)),
                ('cDiscountMaxDiscount', models.DecimalField(decimal_places=3, max_digits=8)),
                ('cDiscountMinOrderValue', models.DecimalField(decimal_places=3, max_digits=8)),
                ('categoryID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Category')),
            ],
            options={
                'db_table': 'cdiscount',
            },
        ),
        migrations.CreateModel(
            name='PDiscount',
            fields=[
                ('pDiscountID', models.AutoField(primary_key=True, serialize=False)),
                ('pDiscountName', models.CharField(max_length=40)),
                ('pDiscountDescription', models.TextField(max_length=200)),
                ('pDiscountType', models.CharField(max_length=30)),
                ('pDiscountValue', models.DecimalField(decimal_places=3, max_digits=8)),
                ('pDiscountDateCreated', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('pDiscountDateValidFrom', models.DateTimeField(verbose_name='valid from')),
                ('pDiscountDateValidUntil', models.DateTimeField(verbose_name='valid until')),
                ('pDiscountCouponCode', models.CharField(max_length=20)),
                ('pDiscountMaxDiscount', models.DecimalField(decimal_places=3, max_digits=8)),
                ('pDiscountMinOrderValue', models.DecimalField(decimal_places=3, max_digits=8)),
                ('productID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Product')),
            ],
            options={
                'db_table': 'pdiscount',
            },
        ),
        migrations.CreateModel(
            name='Pricing',
            fields=[
                ('pricingID', models.AutoField(primary_key=True, serialize=False)),
                ('pricingBasePrice', models.DecimalField(decimal_places=3, max_digits=8)),
                ('pricingDateCreated', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('pricingStartDate', models.DateTimeField(verbose_name='start date')),
                ('pricingEndDate', models.DateTimeField(verbose_name='end date')),
                ('pricingNote', models.TextField(max_length=200)),
                ('productID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Product')),
            ],
            options={
                'db_table': 'pricing',
            },
        ),
    ]
