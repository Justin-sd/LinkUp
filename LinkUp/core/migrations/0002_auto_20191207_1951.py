# Generated by Django 2.2.6 on 2019-12-07 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='duration',
            field=models.IntegerField(default=60),
            preserve_default=False,
        ),
    ]