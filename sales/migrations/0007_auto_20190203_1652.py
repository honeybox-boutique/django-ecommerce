# Generated by Django 2.1.4 on 2019-02-03 16:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0001_initial'),
        ('sales', '0006_auto_20190203_0658'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='saleBillingAddress',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='saleBillingAddress', to='addresses.Address'),
        ),
        migrations.AddField(
            model_name='sale',
            name='saleShippingAddress',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='saleShippingAddress', to='addresses.Address'),
        ),
    ]
