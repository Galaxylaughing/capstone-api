# Generated by Django 3.0.1 on 2020-01-07 02:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_auto_20200107_0038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='series',
            name='planned_count',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
    ]
