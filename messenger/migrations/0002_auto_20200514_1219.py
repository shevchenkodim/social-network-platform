# Generated by Django 3.0.4 on 2020-05-14 09:19

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('messenger', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userchat',
            name='chat_name',
            field=models.CharField(default='default_chat', max_length=128),
        ),
        migrations.AlterField(
            model_name='userchat',
            name='chat_id',
            field=models.UUIDField(default=uuid.UUID('fd614b3e-2740-4607-9179-5971aef3317a')),
        ),
    ]
