# Generated by Django 2.2.4 on 2019-09-07 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pulsa', '0007_auto_20190907_1248'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='cost',
            field=models.FloatField(blank=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='price',
            field=models.FloatField(blank=True),
        ),
    ]
