# Generated by Django 3.2.23 on 2024-02-19 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_auctionlisting_createdby'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='description',
            field=models.TextField(max_length=500),
        ),
        migrations.AlterField(
            model_name='auctionlisting',
            name='urlImage',
            field=models.CharField(max_length=500),
        ),
    ]
