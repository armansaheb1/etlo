# Generated by Django 3.2.3 on 2023-01-24 21:00

from django.db import migrations, models
import django.db.models.deletion
import foreignbuy.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ForeignBuyCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('add_date', models.DateTimeField(auto_now_add=True)),
                ('last_modify_date', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=50, null=True)),
                ('details', models.CharField(max_length=250, null=True)),
                ('icon', models.CharField(max_length=50, null=True)),
                ('image', models.ImageField(null=True, upload_to=foreignbuy.models.PathRename('ForeignBuyCategories', 'ForeignBuyCategories'))),
            ],
            options={
                'verbose_name_plural': ' Foreign Buy Categories ',
            },
        ),
        migrations.CreateModel(
            name='ForeignBuyPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('add_date', models.DateTimeField(auto_now_add=True)),
                ('last_modify_date', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=50, null=True)),
                ('percent_price', models.BooleanField(default=True)),
                ('price', models.FloatField()),
            ],
            options={
                'verbose_name_plural': ' Foreign Buy Posts ',
            },
        ),
        migrations.CreateModel(
            name='ForeignBuyRequests',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('request_id', models.CharField(default=foreignbuy.models.rand, editable=False, max_length=10, unique=True)),
                ('name', models.CharField(max_length=50, null=True)),
                ('details', models.CharField(max_length=250, null=True)),
                ('image', models.URLField()),
                ('link', models.URLField()),
                ('price', models.FloatField()),
                ('weight', models.IntegerField()),
                ('quantity', models.IntegerField()),
                ('payment_status', models.BooleanField()),
                ('status', models.IntegerField(default=0)),
                ('date', models.DateTimeField(auto_now=True)),
                ('sum_price', models.FloatField(blank=True, null=True)),
                ('recieve_date', models.DateTimeField(null=True)),
            ],
            options={
                'verbose_name_plural': ' Foreign Buy Requests ',
            },
        ),
        migrations.CreateModel(
            name='ForeignBuySites',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('add_date', models.DateTimeField(auto_now_add=True)),
                ('last_modify_date', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=50, null=True)),
                ('details', models.CharField(max_length=250, null=True)),
                ('icon', models.CharField(max_length=50, null=True)),
                ('image', models.ImageField(null=True, upload_to=foreignbuy.models.PathRename('ForeignBuyCategories', 'ForeignBuyCategories'))),
                ('link', models.URLField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foreignbuy.foreignbuycategory')),
            ],
            options={
                'verbose_name_plural': ' Foreign Buy Sites ',
            },
        ),
    ]
