# Generated by Django 2.1.4 on 2019-01-21 17:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ProductColorSet',
            new_name='ProductColor',
        ),
        migrations.RenameField(
            model_name='productcolor',
            old_name='productColorSetID',
            new_name='productColorID',
        ),
    ]
