# Generated by Django 2.1.4 on 2019-01-21 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20190121_1715'),
    ]

    operations = [
        migrations.AddField(
            model_name='productcolor',
            name='productColorName',
            field=models.CharField(default='Red', max_length=40),
            preserve_default=False,
        ),
    ]
