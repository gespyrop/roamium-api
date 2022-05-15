# Generated by Django 3.2.13 on 2022-05-14 23:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('routes', '0002_alter_visit_place_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stars', models.IntegerField()),
                ('text', models.TextField()),
                ('visit', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='routes.visit')),
            ],
        ),
    ]