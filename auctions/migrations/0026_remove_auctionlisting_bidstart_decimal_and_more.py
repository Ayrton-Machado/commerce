# Generated by Django 5.2.3 on 2025-06-22 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0025_auctionlisting_bidstart_decimal_bids_bid_decimal'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auctionlisting',
            name='bidstart_decimal',
        ),
        migrations.AlterField(
            model_name='auctionlisting',
            name='bidstart',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
    ]
