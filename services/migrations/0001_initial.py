# Generated by Django 2.2.4 on 2019-08-09 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.CharField(max_length=10)),
                ('type', models.CharField(max_length=10)),
                ('desc', models.CharField(max_length=50)),
                ('cost', models.FloatField()),
                ('price', models.FloatField()),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
