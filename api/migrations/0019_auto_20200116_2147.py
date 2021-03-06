# Generated by Django 3.0.1 on 2020-01-16 21:47

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0018_auto_20200116_1843'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('status_code', models.CharField(choices=[('WTR', 'Want to Read'), ('CURR', 'Currently Reading'), ('COMP', 'Completed'), ('PAUS', 'Paused'), ('DNF', 'Discarded')], max_length=4)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='statuses', to='api.Book')),
            ],
        ),
        migrations.AddIndex(
            model_name='bookstatus',
            index=models.Index(fields=['status_code'], name='status_code_index'),
        ),
    ]
