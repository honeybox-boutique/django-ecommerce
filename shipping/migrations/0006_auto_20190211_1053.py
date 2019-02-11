# Generated by Django 2.1.4 on 2019-02-11 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shipping', '0005_auto_20190211_0953'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shipment',
            name='shipmentCarrier',
            field=models.CharField(choices=[('USPS', 'USPS')], max_length=120),
        ),
        migrations.AlterField(
            model_name='shipment',
            name='shipmentRate',
            field=models.CharField(choices=[('Priority', 'Priority'), ('Express', 'Express')], max_length=120),
        ),
        migrations.AlterField(
            model_name='shipment',
            name='shipmentTrackingNumber',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]