from django.shortcuts import render
from rest_framework import viewsets, filters, permissions, response, status, generics
from django.shortcuts import get_object_or_404
from .models import Articles, Picture
from .serializer import ArticleSerializer, PictureSerializer
from .permission import IsAuthenficatedOnly, IsArticleOwnerOrReadOnly


class ArticleViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenficatedOnly, IsArticleOwnerOrReadOnly)
    # authentication_classes = ()
    filter_backends = (filters.SearchFilter,)

    search_fields = ['id', 'description', 'vendor', 'code', 'name']

    queryset = Articles.objects.all()
    serializer_class = ArticleSerializer

    def create(self, request):

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(added_by=self.request.user)
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)

        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        article = get_object_or_404(Articles, id=pk)
        serializer = self.serializer_class(article, data=request.data)
        if serializer.is_valid():
            serializer.save(updated_by=self.request.user)
            return response.Response(serializer.data, status=status.HTTP_200_OK)

        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PictureView(generics.ListCreateAPIView):
    permission_classes = ()
    authentication_classes = ()
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer
