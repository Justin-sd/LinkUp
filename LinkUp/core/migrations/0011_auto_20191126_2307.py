# Generated by Django 2.2.6 on 2019-11-26 23:07

from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20191126_2305'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='no_earlier_than',
            field=models.DecimalField(decimal_places=2, max_digits=12, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))]),
        ),
        migrations.AlterField(
            model_name='event',
            name='no_later_than',
            field=models.DecimalField(decimal_places=2, max_digits=12, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))]),
        ),
    ]
