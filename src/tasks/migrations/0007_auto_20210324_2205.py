# Generated by Django 3.1.7 on 2021-03-24 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0006_auto_20210320_1545'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('new', 'new'), ('recieved', 'recieved'), ('in_work', 'in work'), ('rejected', 'rejected'), ('complete', 'complete')], default='new', max_length=8, verbose_name='status'),
        ),
    ]
