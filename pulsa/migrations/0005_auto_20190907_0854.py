# Generated by Django 2.2.4 on 2019-09-07 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pulsa', '0004_transaction_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='number',
            field=models.CharField(default='000', max_length=15),
        ),
    ]
