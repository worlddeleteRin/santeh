# Generated by Django 3.0.8 on 2020-10-11 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_attribute_attributeitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='attr',
            field=models.ManyToManyField(to='products.Attribute'),
        ),
    ]
