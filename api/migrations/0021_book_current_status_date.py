# Generated by Django 3.0.1 on 2020-01-17 19:36

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0020_bookstatus_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='current_status_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]