# Generated by Django 4.0.4 on 2022-06-29 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='originalstring',
            name='rates',
            field=models.IntegerField(default=0, verbose_name='Количество оценок'),
        ),
    ]