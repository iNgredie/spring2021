# Generated by Django 3.1.7 on 2021-03-09 15:08

from django.db import migrations, models


def apply_migration(apps, schema_editor):
    ValueWaterGasElectricalMeters = apps.get_model(
        'send_values',
        'ValueWaterGasElectricalMeters'
    )
    objs = []
    for i in ValueWaterGasElectricalMeters.objects.all():
        try:
            i.previous_value = type(i).objects.filter(
                meter=i.meter, pk__lt=i.pk
            ).order_by('pk').last().value
            objs.append(i)
        except AttributeError:
            pass
    ValueWaterGasElectricalMeters.objects.bulk_update(objs, ['previous_value'])


def revert_migration(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('send_values', '0003_auto_20210307_1103'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='valuewatergaselectricalmeters',
            options={'verbose_name': 'Показание счетчика', 'verbose_name_plural': 'Показания счетчиков'},
        ),
        migrations.AlterModelOptions(
            name='watergaselectricalmeters',
            options={'verbose_name': 'Счетчик', 'verbose_name_plural': 'Счетчики'},
        ),
        migrations.AddField(
            model_name='valuewatergaselectricalmeters',
            name='previous_value',
            field=models.PositiveIntegerField(blank=True, default=None, null=True, verbose_name='previous_value'),
        ),
        migrations.RunPython(apply_migration, revert_migration)
    ]
