# Generated by Django 3.2.3 on 2023-02-07 22:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_notification_icon'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='icon',
        ),
    ]
