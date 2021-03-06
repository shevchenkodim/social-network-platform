# Generated by Django 3.0.4 on 2020-04-10 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20200410_1308'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postfilesmodel',
            name='file',
            field=models.FileField(max_length=255, upload_to='posts/image/<django.db.models.query_utils.DeferredAttribute object at 0x000002523091FAC8>/', verbose_name='File'),
        ),
        migrations.AlterField(
            model_name='postsmodel',
            name='hashtag',
            field=models.ManyToManyField(blank=True, related_name='hashtags', to='main.HashtagModel', verbose_name='hashtag'),
        ),
    ]
