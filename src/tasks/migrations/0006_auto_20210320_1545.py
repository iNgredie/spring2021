# Generated by Django 3.1.7 on 2021-03-20 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0005_task_attachment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='task',
            options={'verbose_name': 'task', 'verbose_name_plural': 'tasks'},
        ),
        migrations.AlterField(
            model_name='task',
            name='phone',
            field=models.CharField(max_length=16, verbose_name='phone number'),
        ),
    ]
