# Generated by Django 2.1.4 on 2019-02-21 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0004_card'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='cardDefault',
            field=models.BooleanField(default=False),
        ),
    ]
