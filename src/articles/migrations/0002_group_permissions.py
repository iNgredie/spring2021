# Generated by Django 3.1.7 on 2021-03-20 20:24

from django.db import migrations
from django.core.management.sql import emit_post_migrate_signal


def apply_migration(apps, schema_editor):
    # https://code.djangoproject.com/ticket/23422#comment:28
    # Ensure permissions and content types have been created.
    db_alias = schema_editor.connection.alias
    emit_post_migrate_signal(2, False, db_alias)
    # Now the content types and permissions should exist
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')
    user_permission_list = Permission.objects.filter(codename__in=(
        'view_article',
    ))
    Group.objects.get(name='Жильцы').permissions.add(*user_permission_list)
    tszh_permission_list = Permission.objects.filter(codename__in=(
        'add_article',
        'change_article',
        'delete_article',
        'view_article',
    ))
    Group.objects.get(name='Сотрудники ТСЖ').permissions.add(*tszh_permission_list)


def revert_migration(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')
    user_permission_list = Permission.objects.filter(codename__in=(
        'view_article',
    ))
    Group.objects.get(name='Жильцы').permissions.remove(*user_permission_list)
    tszh_permission_list = Permission.objects.filter(codename__in=(
        'add_article',
        'change_article',
        'delete_article',
        'view_article',
    ))
    Group.objects.get(name='Сотрудники ТСЖ').permissions.remove(*tszh_permission_list)


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0001_initial'),
        ('users', '0003_hardcoded_groups'),
    ]

    operations = [
        migrations.RunPython(apply_migration, revert_migration)
    ]
