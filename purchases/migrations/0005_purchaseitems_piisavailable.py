# Generated by Django 2.1.4 on 2019-02-03 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchases', '0004_auto_20190130_2105'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchaseitems',
            name='piIsAvailable',
            field=models.BooleanField(default=True),
        ),
    ]
