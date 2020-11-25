# Generated by Django 3.0.8 on 2020-10-10 17:44

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
                ('slug', models.CharField(default='', max_length=300)),
                ('name', models.CharField(default='', max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Destination',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=300)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=300)),
                ('price', models.IntegerField(default=0)),
                ('description', models.CharField(default='', max_length=2000)),
                ('imgsrc', models.CharField(default='', max_length=2000)),
                ('category', models.ManyToManyField(to='products.Category')),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Destination')),
            ],
        ),
    ]
