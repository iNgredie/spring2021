from django.db import models
from django.utils.translation import gettext_lazy as _


class DynamicSettings(models.Model):
    """
    Модель справочника
    """
    name = models.CharField(_('name'), max_length=128, unique=True)
    value = models.CharField(_('value'), max_length=128)
    description = models.CharField(_('description'), max_length=256)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'dynamic_settings'
        verbose_name = _('dynamic setting')
        verbose_name_plural = _('dynamic settings')
