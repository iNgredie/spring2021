# Generated by Django 3.1.7 on 2021-03-18 11:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_user_model_permissions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraddress',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='addresses', to=settings.AUTH_USER_MODEL),
        ),
    ]