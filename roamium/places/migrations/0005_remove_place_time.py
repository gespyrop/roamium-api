# Generated by Django 3.2.13 on 2022-09-01 08:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0004_alter_place_wheelchair'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='place',
            name='time',
        ),
    ]
