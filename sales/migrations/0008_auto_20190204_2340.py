# Generated by Django 2.1.4 on 2019-02-04 23:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0007_auto_20190203_1652'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='saleShipCostAmountCharged',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=12),
        ),
    ]
