# Generated by Django 3.2.3 on 2023-02-08 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('insurance', '0010_auto_20230207_2219'),
    ]

    operations = [
        migrations.AddField(
            model_name='healthinsurancerequest',
            name='inid',
            field=models.IntegerField(null=True),
        ),
    ]
