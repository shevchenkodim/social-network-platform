# Generated by Django 3.0.4 on 2020-04-21 19:53

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_delete_commenttestmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='postsmodel',
            name='page_id',
            field=models.UUIDField(default=uuid.uuid4),
        ),
    ]
