# Generated by Django 3.0.1 on 2020-01-06 19:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_series_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='series',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='books', to='api.Series'),
        ),
    ]
