# Generated by Django 2.1.4 on 2019-01-31 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pricing', '0002_auto_20190128_1841'),
    ]

    operations = [
        migrations.AddField(
            model_name='pricing',
            name='pricingIsActive',
            field=models.BooleanField(default=False),
        ),
    ]