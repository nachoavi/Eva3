# Generated by Django 4.2.7 on 2023-11-23 02:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_remove_order_productsincart'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='products',
            field=models.ManyToManyField(to='app.products'),
        ),
    ]
