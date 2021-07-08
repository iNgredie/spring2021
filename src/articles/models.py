from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


CustomUser = get_user_model()


def article_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/article/<date>/<filename>
    return 'article/{0:%Y-%m-%d}/{1}'.format(instance.created_at, filename)


class Article(models.Model):
    """
    Модель новостей
    """
    title = models.CharField(_('title'), max_length=120)
    content = models.TextField(_('content'))
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    author = models.ForeignKey(
        CustomUser,
        related_name='news',
        on_delete=models.CASCADE,
        verbose_name=_('author')
    )
    image = models.ImageField(
        _('image'),
        upload_to=article_path,
        null=True,
        blank=True,
        default=None,
    )

    @property
    def preview(self):
        if len(self.content) > 247:
            return '{}...'.format(self.content[:247])
        return self.content

    preview.fget.short_description = _('preview')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('article')
        verbose_name_plural = _('articles')
