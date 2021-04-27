# Generated by Django 3.2 on 2021-04-26 20:25

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('location', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('time', models.DurationField()),
                ('is_bike', models.BooleanField(default=False)),
                ('is_wheelchair', models.BooleanField(default=False)),
                ('is_family', models.BooleanField(default=False)),
                ('is_friends', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'place',
                'verbose_name_plural': 'places',
            },
        ),
    ]
