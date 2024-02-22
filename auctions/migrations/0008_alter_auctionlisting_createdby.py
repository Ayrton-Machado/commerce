# Generated by Django 3.2.23 on 2024-02-20 00:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_alter_auctionlisting_createdby'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='createdBy',
            field=models.ForeignKey(blank=True, max_length=64, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
