# Generated by Django 3.0.8 on 2020-10-22 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_auto_20201011_2009'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='sale_price',
            field=models.IntegerField(default=0),
        ),
    ]
