# Generated by Django 2.1.4 on 2019-01-21 16:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PurchaseItems',
            fields=[
                ('prodStockID', models.AutoField(primary_key=True, serialize=False)),
                ('piPrice', models.DecimalField(decimal_places=3, max_digits=8)),
                ('piSize', models.CharField(max_length=20)),
                ('piColor', models.CharField(max_length=40)),
                ('piCondition', models.CharField(max_length=50)),
                ('piNotes', models.TextField(max_length=200)),
                ('piBarcode', models.ImageField(upload_to='barcodes')),
                ('productID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Product')),
            ],
            options={
                'db_table': 'purchase_items',
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('transactionID', models.AutoField(primary_key=True, serialize=False)),
                ('transactionDate', models.DateTimeField(verbose_name='date purchased')),
                ('transactionNote', models.TextField(max_length=200)),
                ('transactionStatus', models.CharField(max_length=40)),
                ('productID', models.ManyToManyField(through='purchases.PurchaseItems', to='products.Product')),
            ],
            options={
                'db_table': 'transaction',
            },
        ),
        migrations.CreateModel(
            name='TransactionType',
            fields=[
                ('transactionTypeID', models.AutoField(primary_key=True, serialize=False)),
                ('transactionTypeName', models.CharField(max_length=40)),
                ('transactionTypeDescription', models.TextField(max_length=200)),
            ],
            options={
                'db_table': 'transaction_type',
            },
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('vendorID', models.AutoField(primary_key=True, serialize=False)),
                ('vendorName', models.CharField(max_length=40)),
                ('vendorDescription', models.TextField(max_length=200)),
                ('vendorNotes', models.TextField(max_length=200)),
                ('vendorWebsite', models.URLField()),
            ],
            options={
                'db_table': 'vendor',
            },
        ),
        migrations.AddField(
            model_name='transaction',
            name='transactionTypeID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='purchases.TransactionType'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='userID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='purchaseitems',
            name='transactionID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='purchases.Transaction'),
        ),
        migrations.AddField(
            model_name='purchaseitems',
            name='vendorID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='purchases.Vendor'),
        ),
    ]
