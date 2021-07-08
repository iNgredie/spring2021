# Generated by Django 3.1.7 on 2021-03-06 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DynamicSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True, verbose_name='name')),
                ('value', models.CharField(max_length=128, verbose_name='value')),
                ('description', models.CharField(max_length=256, verbose_name='description')),
            ],
            options={
                'db_table': 'dynamic_settings',
            },
        ),
    ]
