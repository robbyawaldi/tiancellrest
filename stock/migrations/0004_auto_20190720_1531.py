# Generated by Django 2.2.3 on 2019-07-20 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0003_auto_20190720_1528'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]