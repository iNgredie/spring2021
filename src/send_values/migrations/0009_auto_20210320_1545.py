# Generated by Django 3.1.7 on 2021-03-20 15:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('send_values', '0008_watergaselectricalmeters_address'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='meterstype',
            options={'verbose_name': 'meter type', 'verbose_name_plural': 'meter types'},
        ),
        migrations.AlterModelOptions(
            name='valuewatergaselectricalmeters',
            options={'verbose_name': 'meter value', 'verbose_name_plural': 'meter values'},
        ),
        migrations.AlterModelOptions(
            name='watergaselectricalmeters',
            options={'verbose_name': 'meter', 'verbose_name_plural': 'meters'},
        ),
        migrations.AlterField(
            model_name='valuewatergaselectricalmeters',
            name='meter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='meter', to='send_values.watergaselectricalmeters', verbose_name='meter'),
        ),
        migrations.AlterField(
            model_name='valuewatergaselectricalmeters',
            name='previous_value',
            field=models.PositiveIntegerField(blank=True, default=None, null=True, verbose_name='previous value'),
        ),
        migrations.AlterField(
            model_name='valuewatergaselectricalmeters',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
        migrations.AlterField(
            model_name='watergaselectricalmeters',
            name='meters_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='send_values.meterstype', verbose_name='meter type'),
        ),
        migrations.AlterField(
            model_name='watergaselectricalmeters',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
    ]
