# Generated by Django 2.1.4 on 2019-02-11 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0002_auto_20190206_2104'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='addressEasyPostID',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]