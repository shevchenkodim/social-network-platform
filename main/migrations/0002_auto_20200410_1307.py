# Generated by Django 3.0.4 on 2020-04-10 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postfilesmodel',
            name='file',
            field=models.FileField(max_length=255, upload_to='posts/image/<django.db.models.query_utils.DeferredAttribute object at 0x000001DE1D3CFAC8>/', verbose_name='File'),
        ),
    ]
