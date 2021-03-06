# Generated by Django 2.1.4 on 2019-01-21 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ShoppingCart',
            fields=[
                ('shoppingCartID', models.AutoField(primary_key=True, serialize=False)),
                ('vendorName', models.CharField(max_length=40)),
                ('vendorDescription', models.TextField(max_length=200)),
                ('vendorNotes', models.TextField(max_length=200)),
                ('vendorWebsite', models.URLField()),
            ],
            options={
                'db_table': 'shopping_cart',
            },
        ),
    ]
