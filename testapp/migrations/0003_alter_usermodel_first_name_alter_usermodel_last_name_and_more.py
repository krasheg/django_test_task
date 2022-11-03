# Generated by Django 4.1.3 on 2022-11-02 21:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0002_alter_usermodel_date_joined'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermodel',
            name='first_name',
            field=models.CharField(blank=True, max_length=16),
        ),
        migrations.AlterField(
            model_name='usermodel',
            name='last_name',
            field=models.CharField(blank=True, max_length=16),
        ),
        migrations.AlterField(
            model_name='usermodel',
            name='photo_url',
            field=models.URLField(blank=True, max_length=255),
        ),
    ]