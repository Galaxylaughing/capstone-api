# Generated by Django 3.0.1 on 2020-01-13 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_bookauthor_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='isbn_10',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='isbn_13',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='page_count',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='publication_date',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='publisher',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
