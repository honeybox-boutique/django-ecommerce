# Generated by Django 2.1.7 on 2019-02-24 04:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0003_address_addresseasypostid'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='addressActive',
            field=models.BooleanField(default=True),
        ),
    ]