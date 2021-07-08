import datetime
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from src.users.models import UserAddress


User = get_user_model()


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class TaskStatus(models.Model):
    """
    Модель статусов заявок
    """

    title = models.CharField(_('title'), max_length=100)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'task_status'
        verbose_name = _('task status')
        verbose_name_plural = _('task statuses')


class Task(models.Model):
    """
    Модель заявок
    """
    subject = models.CharField(_('subject'), max_length=128)
    text = models.TextField(_('text'))
    created_at = models.DateTimeField(_('created_at'), auto_now_add=True)
    completed_at = models.DateTimeField(_('completed_at'), null=True, default=None)
    task_status = models.ForeignKey(
        TaskStatus,
        on_delete=models.CASCADE,
        verbose_name=_('status'),
        related_name='statuses',
        default=1,  # статус "новый"
    )

    surname = models.CharField(_('surname'), max_length=100)
    name = models.CharField(_('name'), max_length=100)
    patronymic = models.CharField(_('patronymic'), max_length=100, blank=True, null=True)
    phone = models.CharField(_('phone number'), max_length=16)
    email = models.EmailField(_('email'), blank=True, null=True)

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('user'),
        related_name='users'
    )
    performer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('performer'),
        related_name='performers',
        null=True,
        default=None
    )
    address = models.ForeignKey(
        UserAddress,
        on_delete=models.CASCADE,
        verbose_name=_('address'),
        related_name='addresses',
    )
    attachment = models.ImageField(
        _('attachment'),
        upload_to=user_directory_path,
        null=True,
        blank=True,
        default=None,
    )

    def __str__(self):
        return f'{self.subject} created_at {self.created_at} by {self.user}'

    def save(self, *args, **kwargs):
        if self.task_status.title == 'Новая' and not self.completed_at:
            self.completed_at = datetime.datetime.now()
        return super().save(*args, **kwargs)

    class Meta:
        db_table = 'task'
        verbose_name = _('task')
        verbose_name_plural = _('tasks')
