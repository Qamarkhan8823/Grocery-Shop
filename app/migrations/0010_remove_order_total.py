# Generated by Django 4.1.7 on 2023-04-19 15:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_order_total'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='total',
        ),
    ]
