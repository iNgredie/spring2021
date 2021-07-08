from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from src.users.models import UserAddress

User = get_user_model()


class Service(models.Model):
    """
    Модель услуг
    """
    text = models.CharField(_('text'), max_length=2000)
    created_at = models.DateTimeField(_('created_at'), auto_now_add=True)

    surname = models.CharField(_('surname'), max_length=100)
    name = models.CharField(_('name'), max_length=100)
    patronymic = models.CharField(_('patronymic'), max_length=100, blank=True, null=True)
    phone = models.CharField(_('phone number'), max_length=16)
    email = models.EmailField(_('email'), blank=True, null=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('user'),
        related_name='service_users'
    )
    address = models.ForeignKey(
        UserAddress,
        on_delete=models.CASCADE,
        verbose_name=_('address'),
        related_name='service_addresses',
    )

    def __str__(self):
        return f'Услуга: {self.text[:30]}... заказана {self.user} : {self.created_at}'

    class Meta:
        db_table = 'service'
        verbose_name = _('service')
        verbose_name_plural = _('services')


class PriceList(models.Model):
    """
    Модель прайс листа услуг
    """
    name = models.CharField(_('name'), max_length=1000)
    price = models.PositiveIntegerField(_('price'))

    def __str__(self):
        return f'{self.name} : {self.price}'

    class Meta:
        db_table = 'price_list'
        verbose_name = _('price list')
        verbose_name_plural = _('price lists')
