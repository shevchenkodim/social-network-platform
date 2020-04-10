# Generated by Django 3.0.4 on 2020-04-10 10:07

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('signup', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='folowers',
            field=models.ManyToManyField(blank=True, null=True, related_name='folowers', to=settings.AUTH_USER_MODEL, verbose_name='folower'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='folowing',
            field=models.ManyToManyField(blank=True, null=True, related_name='folows', to=settings.AUTH_USER_MODEL, verbose_name='folow'),
        ),
    ]
