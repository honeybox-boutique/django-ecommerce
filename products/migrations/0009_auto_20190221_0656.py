# Generated by Django 2.1.4 on 2019-02-21 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_auto_20190218_2231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='productDescription',
            field=models.TextField(max_length=200),
        ),
    ]