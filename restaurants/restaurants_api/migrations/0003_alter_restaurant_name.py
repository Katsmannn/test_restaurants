# Generated by Django 3.2.12 on 2022-02-23 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants_api', '0002_auto_20220223_1203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='name',
            field=models.CharField(max_length=50, verbose_name='name'),
        ),
    ]