# Generated by Django 3.1.7 on 2021-03-16 18:56

from django.db import migrations, models
import django.db.models.deletion


def apply_migration(apps, schema_editor):
    MetersType = apps.get_model('send_values', 'MetersType')

    MetersType.objects.bulk_create([
        MetersType(title='Холодная вода', measure='м³'),
        MetersType(title='Горячая вода', measure='м³'),
        MetersType(title='Газ', measure='м³'),
        MetersType(title='Электричество', measure='кВт·ч'),
    ])


def revert_migration(apps, schema_editor):
    MetersType = apps.get_model('send_values', 'MetersType')

    MetersType.objects.filter(title__in=[
        'Холодная вода',
        'Горячая вода',
        'Газ',
        'Электричество',
    ]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('send_values', '0005_watergaselectricalmeters_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='MetersType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='title')),
                ('measure', models.CharField(max_length=100, verbose_name='measure')),
            ],
            options={
                'verbose_name': 'Тип счетчика',
                'verbose_name_plural': 'Типы счетчиков',
            },
        ),
        migrations.AddField(
            model_name='watergaselectricalmeters',
            name='meters_type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='send_values.meterstype'),
            preserve_default=False,
        ),
        migrations.RunPython(apply_migration, revert_migration),
    ]
