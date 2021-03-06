# Generated by Django 2.1.4 on 2019-02-21 10:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0003_billingprofile_billingtoken'),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cardStripeID', models.CharField(max_length=120)),
                ('cardBrand', models.CharField(blank=True, max_length=120, null=True)),
                ('cardCountry', models.CharField(blank=True, max_length=20, null=True)),
                ('cardExpMonth', models.IntegerField(blank=True, null=True)),
                ('cardExpYear', models.IntegerField(blank=True, null=True)),
                ('cardLast4', models.CharField(max_length=4)),
                ('billingProfile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='billing.BillingProfile')),
            ],
            options={
                'db_table': 'card',
            },
        ),
    ]
