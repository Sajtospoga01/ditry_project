# Generated by Django 2.2.26 on 2022-03-08 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='original',
            field=models.IntegerField(null=True),
        ),
    ]
