# Generated by Django 4.2.6 on 2024-02-23 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_productprice_loyalty_card_deal_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='productprice',
            name='rrp_price_per_weight',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
