# Generated by Django 2.1.4 on 2019-02-08 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0002_auto_20190130_2100'),
    ]

    operations = [
        migrations.AddField(
            model_name='billingprofile',
            name='billingToken',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]
