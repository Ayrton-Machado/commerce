# Generated by Django 3.2.23 on 2024-02-21 20:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_alter_category_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='category',
        ),
        migrations.AddField(
            model_name='auctionlisting',
            name='category',
            field=models.ForeignKey(blank=True, max_length=64, on_delete=django.db.models.deletion.CASCADE, to='auctions.category'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='category',
            name='categories',
            field=models.CharField(default=True, max_length=64),
            preserve_default=False,
        ),
    ]
