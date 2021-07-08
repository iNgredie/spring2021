# Generated by Django 3.1.7 on 2021-03-26 09:59

from django.db import migrations, models
import django.db.models.deletion


def to_new_statuses(apps, schema_editor):
    TaskStatus = apps.get_model('tasks', 'TaskStatus')
    Task = apps.get_model('tasks', 'Task')

    TaskStatus.objects.bulk_create([
        TaskStatus(title='Новая'),
        TaskStatus(title='Принята'),
        TaskStatus(title='В работе'),
        TaskStatus(title='Отклонена'),
        TaskStatus(title='Исполнена'),
    ])

    Task.objects.filter(status='new').update(
        task_status=TaskStatus.objects.get(title='Новая')
    )
    Task.objects.filter(status='recieved').update(
        task_status=TaskStatus.objects.get(title='Принята')
    )
    Task.objects.filter(status='in work').update(
        task_status=TaskStatus.objects.get(title='В работе')
    )
    Task.objects.filter(status='rejected').update(
        task_status=TaskStatus.objects.get(title='Отклонена')
    )
    Task.objects.filter(status='complete').update(
        task_status=TaskStatus.objects.get(title='Исполнена')
    )


def to_old_statuses(apps, schema_editor):
    TaskStatus = apps.get_model('tasks', 'TaskStatus')
    Task = apps.get_model('tasks', 'Task')

    Task.objects.filter(task_status__title='Новая').update(status='new')
    Task.objects.filter(task_status__title='Принята').update(status='recieved')
    Task.objects.filter(task_status__title='В работе').update(status='in work')
    Task.objects.filter(task_status__title='Отклонена').update(status='rejected')
    Task.objects.filter(task_status__title='Исполнена').update(status='complete')

    TaskStatus.objects.filter(title__in=[
        'Новая',
        'Принята',
        'В работе',
        'Отклонена',
        'Исполнена',
    ]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0009_auto_20210325_1944'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='title')),
            ],
            options={
                'db_table': 'task_status',
                'verbose_name': 'task status',
                'verbose_name_plural': 'task statuses',
            },
        ),
        migrations.AddField(
            model_name='task',
            name='task_status',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='statuses', to='tasks.taskstatus', verbose_name='status'),
        ),
        migrations.RunPython(to_new_statuses, to_old_statuses),
        migrations.RemoveField(
            model_name='task',
            name='status',
        ),
        migrations.AlterField(
            model_name='task',
            name='task_status',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='statuses', to='tasks.taskstatus', verbose_name='status'),
        ),
    ]