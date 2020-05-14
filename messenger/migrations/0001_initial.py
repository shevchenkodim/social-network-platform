# Generated by Django 3.0.4 on 2020-05-14 08:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserChat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_create', models.DateTimeField(auto_now_add=True)),
                ('chat_id', models.UUIDField(default=uuid.UUID('f84fe59a-4f08-4dfc-9de9-ce5cc3963548'))),
            ],
        ),
        migrations.CreateModel(
            name='UsersInChat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chat_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='messenger.UserChat')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserMessages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=1024)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('from_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_id', to=settings.AUTH_USER_MODEL)),
                ('to_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_id', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
