# Generated by Django 3.2.13 on 2022-07-05 08:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='created',
        ),
    ]
