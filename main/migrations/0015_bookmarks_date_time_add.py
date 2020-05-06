# Generated by Django 3.0.4 on 2020-05-06 18:55

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_bookmarks'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookmarks',
            name='date_time_add',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Date and time add'),
            preserve_default=False,
        ),
    ]
