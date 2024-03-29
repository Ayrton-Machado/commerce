# Generated by Django 3.2.23 on 2024-02-20 01:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_alter_auctionlisting_createdby'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='bidstart',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='auctionlisting',
            name='category',
            field=models.CharField(blank=True, max_length=64),
        ),
        migrations.AlterField(
            model_name='auctionlisting',
            name='description',
            field=models.TextField(blank=True, max_length=500),
        ),
        migrations.AlterField(
            model_name='auctionlisting',
            name='title',
            field=models.CharField(blank=True, max_length=64),
        ),
        migrations.AlterField(
            model_name='auctionlisting',
            name='urlImage',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]
