# Generated by Django 3.0.8 on 2020-10-22 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0003_item_imgsrc'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='sale_price',
            field=models.IntegerField(default=0),
        ),
    ]