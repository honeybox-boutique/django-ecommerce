# Generated by Django 2.1.7 on 2019-02-27 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0005_address_addressname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='addressCountry',
            field=models.CharField(choices=[('United States', 'United States')], default='United States', max_length=120),
        ),
        migrations.AlterField(
            model_name='address',
            name='addressState',
            field=models.CharField(choices=[('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('FL', 'Florida'), ('GA', 'Georgia'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming'), ('AS', 'American Samoa'), ('DC', 'District of Columbia'), ('FM', 'Federated States of Micronesia'), ('GU', 'Guam'), ('MH', 'Marshall Islands'), ('MP', 'Northern Mariana Islands'), ('PW', 'Palau'), ('PR', 'Puerto Rico'), ('VI', 'Virgin Islands')], max_length=120),
        ),
    ]
