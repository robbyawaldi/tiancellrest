# Generated by Django 2.2.4 on 2019-09-07 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pulsa', '0006_auto_20190907_0910'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='transaction',
            options={'ordering': ['-date']},
        ),
        migrations.AlterField(
            model_name='transaction',
            name='cost',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='price',
            field=models.FloatField(),
        ),
    ]
