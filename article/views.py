from django.shortcuts import render
from rest_framework import viewsets, filters, permissions, response, status, generics
from django.shortcuts import get_object_or_404
from .models import Articles, Picture
from .serializer import ArticleSerializer, PictureSerializer
from .permission import IsAuthenficatedOnly, IsArticleOwnerOrReadOnly
from helpers.view import CreateUpdateMixin


class ArticleViewSet(CreateUpdateMixin, viewsets.ModelViewSet, ):
    permission_classes = (IsAuthenficatedOnly, IsArticleOwnerOrReadOnly)
    # authentication_classes = ()
    filter_backends = (filters.SearchFilter,)

    search_fields = ['id', 'description', 'vendor', 'code', 'name']

    queryset = Articles.objects.all()
    serializer_class = ArticleSerializer
    Object = Articles


class PictureView(generics.ListCreateAPIView):
    permission_classes = ()
    authentication_classes = ()
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer
