# Generated by Django 5.2.3 on 2025-06-22 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0026_remove_auctionlisting_bidstart_decimal_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bids',
            name='bid_decimal',
        ),
        migrations.AlterField(
            model_name='bids',
            name='bid',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
    ]
