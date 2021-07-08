from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, Group
from django.utils.translation import gettext_lazy as _

from django.db import models
from django.utils import timezone

from .managers import CustomUserManager


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/ownership/<filename>
    return 'user_{0}/ownership/{1}'.format(instance.id, filename)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom user. Client. Customer.
    """
    mobile = models.CharField(_('phone number'), max_length=16, unique=True)
    email = models.EmailField(_('email address'), blank=True, null=True)
    surname = models.CharField(_('surname'), max_length=100, blank=True, null=True)
    name = models.CharField(_('name'), max_length=100, blank=True, null=True)
    patronymic = models.CharField(_('patronymic'), max_length=100, blank=True, null=True)
    is_staff = models.BooleanField(_('is staff'), default=False)
    is_active = models.BooleanField(_('is active'), default=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    personal_account = models.CharField(_('personal account'), max_length=255, blank=True, null=True)
    attachment = models.FileField(
        _('attachment'),
        upload_to=user_directory_path,
        null=True,
        blank=True,
        default=None,
    )

    USERNAME_FIELD = 'mobile'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        is_new = self.pk is None and not self.is_superuser
        super().save(*args, **kwargs)
        if is_new:
            self.groups.add(
                Group.objects.get(name='Жильцы')
            )

    def __str__(self):
        return self.mobile or self.email

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')


class UserAddress(models.Model):
    """
    Адрес жильца
    """
    street = models.CharField(_('street'), max_length=255)
    house = models.CharField(_('house'), max_length=10)
    building = models.CharField(_('building'), max_length=10, blank=True, null=True)
    apartment = models.CharField(_('apartment'), max_length=10, blank=True, null=True)
    is_main = models.BooleanField(_('main user address'), default=False)
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='addresses',
        verbose_name=_('user')
    )

    def save(self, *args, **kwargs):
        """
        Проверка на уникальность поля is_main,
        при сохранение
        Возможен только один основной адрес
        """
        if self.is_main:
            self.user.addresses.update(is_main=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.street}, {self.house}, {self.apartment}, {self.user.name}'

    class Meta:
        verbose_name = _('user address')
        verbose_name_plural = _('user addresses')
