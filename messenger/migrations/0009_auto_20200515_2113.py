# Generated by Django 3.0.4 on 2020-05-15 18:13

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('messenger', '0008_auto_20200514_2251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userchat',
            name='chat_id',
            field=models.UUIDField(default=uuid.UUID('73f0d143-57ab-4da6-b05f-c60667f824e9')),
        ),
    ]