# Generated by Django 3.1.3 on 2020-12-12 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0013_attributeitem_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='imgsrc',
            field=models.ImageField(blank=True, default=None, upload_to='static/images/products'),
        ),
    ]
