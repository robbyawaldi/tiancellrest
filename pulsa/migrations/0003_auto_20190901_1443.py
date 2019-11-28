# Generated by Django 2.2.4 on 2019-09-01 14:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pulsa', '0002_transaction_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nominal',
            name='provider',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nominals', to='pulsa.Provider'),
        ),
    ]