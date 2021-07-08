from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from src.users.models import UserAddress


User = get_user_model()


class MetersType(models.Model):
    """
    Тип счетчика
    """
    title = models.CharField(_('title'), max_length=100)
    measure = models.CharField(_('measure'), max_length=100)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('meter type')
        verbose_name_plural = _('meter types')


class WaterGasElectricalMeters(models.Model):
    """
    Домовой счетчик
    """
    title = models.CharField(_('title'), max_length=100)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('user'),
    )
    meters_type = models.ForeignKey(
        MetersType,
        on_delete=models.CASCADE,
        verbose_name=_('meter type'),
    )
    address = models.ForeignKey(
        UserAddress,
        on_delete=models.CASCADE,
        verbose_name=_('address'),
        related_name='meter_address',
        null=True,
        blank=True,
        default=None,
    )

    @property
    def previous_value(self):
        try:
            return self.meter.order_by('pk').last().value
        except AttributeError:
            return None

    previous_value.fget.short_description = _('previous value')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('meter')
        verbose_name_plural = _('meters')


class ValueWaterGasElectricalMeters(models.Model):
    """
    Показания домового счетчика
    """
    value = models.PositiveIntegerField(_('value'))
    previous_value = models.PositiveIntegerField(
        _('previous value'),
        null=True,
        blank=True,
        default=None
    )
    meter = models.ForeignKey(
        WaterGasElectricalMeters,
        on_delete=models.CASCADE,
        related_name='meter',
        verbose_name=_('meter'),
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user',
        verbose_name=_('user'),
    )
    date = models.DateTimeField(_('sending date'), auto_now_add=True)

    def save(self, *args, **kwargs):
        try:
            self.previous_value = type(self).objects.filter(
                meter=self.meter
            ).order_by('pk').last().value
        except AttributeError:
            pass
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.meter}: {self.value}'

    class Meta:
        verbose_name = _('meter value')
        verbose_name_plural = _('meter values')
