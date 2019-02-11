# Generated by Django 2.1.4 on 2019-02-11 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shipping', '0002_auto_20190211_0714'),
    ]

    operations = [
        migrations.AddField(
            model_name='shipment',
            name='shipmentLabelURL',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='parcel',
            name='parcelName',
            field=models.CharField(choices=[('card', 'Card'), ('letter', 'Letter'), ('flat', 'Flat'), ('flatRateEnvelope', 'FlatRateEnvelope'), ('flatRateLegalEnvelope', 'FlatRateLegalEnvelope'), ('flatRatePaddedEnvelope', 'FlatRatePaddedEnvelope'), ('parcel', 'Parcel'), ('irregularParcel', 'IrregularParcel'), ('softPack', 'SoftPack'), ('smallFlatRateBox', 'SmallFlatRateBox'), ('mediumFlatRateBox', 'MediumFlatRateBox'), ('largeFlatRateBox', 'LargeFlatRateBox'), ('largeFlatRateBoxAPOFPO', 'LargeFlatRateBoxAPOFPO'), ('regionalRateBoxA', 'RegionalRateBoxA'), ('regionalRateBoxB', 'RegionalRateBoxB')], max_length=120),
        ),
        migrations.AlterField(
            model_name='shipment',
            name='shipmentCarrier',
            field=models.CharField(choices=[('usps', 'USPS')], max_length=120),
        ),
        migrations.AlterField(
            model_name='shipment',
            name='shipmentRate',
            field=models.CharField(choices=[('priority', 'Priority'), ('express', 'Express')], max_length=120),
        ),
    ]