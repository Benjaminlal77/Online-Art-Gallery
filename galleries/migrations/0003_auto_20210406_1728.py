# Generated by Django 3.1.7 on 2021-04-06 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('galleries', '0002_auto_20210402_1704'),
    ]

    operations = [
        migrations.AddField(
            model_name='mediaupload',
            name='artist',
            field=models.CharField(default='Unknown', max_length=100),
        ),
        migrations.AlterField(
            model_name='mediaupload',
            name='title',
            field=models.CharField(default='Untitled', max_length=200),
        ),
    ]
