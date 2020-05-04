# Generated by Django 3.0.4 on 2020-05-04 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signup', '0007_auto_20200426_1031'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='is_show_current_city',
            field=models.BooleanField(default=True, verbose_name='Show info current city in user page any user'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='is_show_home_town',
            field=models.BooleanField(default=True, verbose_name='Show info home town in user page any user'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='is_show_phone_number',
            field=models.BooleanField(default=True, verbose_name='Show info phone number in user page any user'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='is_show_relationship',
            field=models.BooleanField(default=True, verbose_name='Show info relationship in user page any user'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='is_show_studied',
            field=models.BooleanField(default=True, verbose_name='Show info studied in user page any user'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='is_show_work',
            field=models.BooleanField(default=True, verbose_name='Show info work in user page any user'),
        ),
    ]