# Generated by Django 3.0.4 on 2020-04-16 13:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_commenttestmodel'),
    ]

    operations = [
        migrations.RenameField(
            model_name='commenttestmodel',
            old_name='reply_to',
            new_name='parent',
        ),
    ]
