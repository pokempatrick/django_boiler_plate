from rest_framework import serializers
from authentification.serializer import RegisterSerilizer
from article.models import Articles


class ArticleSerializer(serializers.ModelSerializer):
    added_by = RegisterSerilizer(
        read_only=True, default=None)

    class Meta:
        model = Articles
        fields = '__all__'
