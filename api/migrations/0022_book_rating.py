# Generated by Django 3.0.1 on 2020-01-19 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0021_book_current_status_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='rating',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Unrated'), (1, 'One'), (2, 'Two'), (3, 'Three'), (4, 'Four'), (5, 'Five')], default=0),
        ),
    ]