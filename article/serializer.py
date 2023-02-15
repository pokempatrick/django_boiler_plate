from rest_framework import serializers
from authentification.serializer import RegisterSerilizer
from article.models import Articles, Picture


class ArticleSerializer(serializers.ModelSerializer):
    added_by = RegisterSerilizer(
        read_only=True, default=None)

    updated_by = RegisterSerilizer(
        read_only=True, default=None)

    class Meta:
        model = Articles
        fields = '__all__'


class PictureSerializer(serializers.ModelSerializer):

    class Meta:
        model = Picture
        fields = ('title', 'file')
