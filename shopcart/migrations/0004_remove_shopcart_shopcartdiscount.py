# Generated by Django 2.1.4 on 2019-02-04 23:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shopcart', '0003_auto_20190130_2100'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shopcart',
            name='shopCartDiscount',
        ),
    ]
