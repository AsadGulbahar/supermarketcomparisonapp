# Generated by Django 4.2.6 on 2024-04-18 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_order_shippingaddress_orderitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='shoppinglist',
            name='last_modified',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
