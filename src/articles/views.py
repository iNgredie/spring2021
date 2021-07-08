from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.pagination import PageNumberPagination
from drf_spectacular.utils import extend_schema_view, extend_schema

from src.users.mixins import MultiSerializerViewSetMixin
from .models import Article
from .serializers import ArticleSerializer, ArticlePreviewSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


@extend_schema_view(
    create=extend_schema(description='Создание новости'),
    retrieve=extend_schema(description='Получение новости'),
    update=extend_schema(description='Полное обновление новости'),
    partial_update=extend_schema(description='Частичное обновление новости'),
    destroy=extend_schema(description='Удаление новости'),
    list=extend_schema(description='Получение списка новостей'),
)
class ArticleViewSet(MultiSerializerViewSetMixin, ModelViewSet):
    """
    CRUD для новостей
    """
    queryset = Article.objects.order_by('-created_at')
    serializer_class = ArticleSerializer
    permission_classes = (DjangoModelPermissions, )
    pagination_class = StandardResultsSetPagination

    serializer_action_classes = {
        'list': ArticlePreviewSerializer,
    }

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
