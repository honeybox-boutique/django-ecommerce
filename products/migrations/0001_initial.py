# Generated by Django 2.1.4 on 2019-01-14 23:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categoryName', models.CharField(max_length=200)),
                ('categoryDescription', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'category',
            },
        ),
        migrations.CreateModel(
            name='CategoryImage',
            fields=[
                ('categoryImageID', models.AutoField(primary_key=True, serialize=False)),
                ('categoryImagePath', models.ImageField(upload_to='categories')),
                ('categoryID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Category')),
            ],
            options={
                'db_table': 'category_image',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('productID', models.AutoField(primary_key=True, serialize=False)),
                ('productName', models.CharField(max_length=200)),
                ('productDescription', models.CharField(max_length=200)),
                ('productCategories', models.ManyToManyField(to='products.Category')),
            ],
            options={
                'db_table': 'product',
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('productImageID', models.AutoField(primary_key=True, serialize=False)),
                ('productImagePath', models.ImageField(upload_to='products')),
                ('productID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Product')),
            ],
            options={
                'db_table': 'product_image',
            },
        ),
    ]
