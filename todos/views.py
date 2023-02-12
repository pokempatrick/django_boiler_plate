from django.shortcuts import render, get_object_or_404
from rest_framework.generics import GenericAPIView
from rest_framework import response, status, permissions, viewsets
from todos.models import Todos
from todos.serializer import TodoSerilizer

# Create your views here.


class TodoAPIView(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    # authentication_classes = ()
    serializer_class = TodoSerilizer

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=self.request.user)
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)

        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, id=None):
        if id:
            todo = get_object_or_404(Todos, id=id)

            serializer = self.serializer_class(todo)
            return response.Response(serializer.data)

        todos = Todos.objects.filter(owner=self.request.user)

        serializer = self.serializer_class(todos, many=True)

        return response.Response(serializer.data)

    def put(self, request, id=None):
        todo = get_object_or_404(Todos, id=id)
        serializer = self.serializer_class(todo, data=request.data)
        if serializer.is_valid():
            serializer.save(owner=self.request.user)
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)

        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id=None):

        todo = get_object_or_404(Todos, id=id)

        todo.delete()

        return response.Response({"message": "object deleted"}, status=status.HTTP_400_BAD_REQUEST)
