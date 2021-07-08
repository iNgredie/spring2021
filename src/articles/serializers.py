from rest_framework import serializers
from .models import Article


class ArticleSerializer(serializers.ModelSerializer):
    """
    Сериализатор для новостей.
    """

    class Meta:
        model = Article
        fields = ('pk', 'title', 'content', 'created_at', 'image')
        read_only_fields = ('created_at', 'author')


class ArticlePreviewSerializer(serializers.ModelSerializer):
    """
    Сериализатор для новостей с урезанным текстом.
    """
    preview = serializers.CharField(read_only=True)

    class Meta:
        model = Article
        fields = ('pk', 'title', 'preview', 'created_at', 'image')
        read_only_fields = ('created_at', 'author', 'preview')
