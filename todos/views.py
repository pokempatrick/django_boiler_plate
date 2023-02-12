from django.shortcuts import get_object_or_404
from rest_framework.generics import GenericAPIView
from rest_framework import response, status, permissions
from todos.models import Todos
from todos.serializer import TodoSerilizer
from rest_framework.settings import api_settings

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

    def get(self, request, id=None, limit=10, page=1):
        if id:
            todo = get_object_or_404(Todos, id=id)
            serializer = self.serializer_class(todo)

            return response.Response(serializer.data)

        todos = Todos.objects.filter(owner=self.request.user)
        if request.query_params and request.query_params["limit"]:
            limit = request.query_params["limit"]
        if request.query_params and request.query_params["page"]:
            page = request.query_params["page"]

        serializer = self.serializer_class(todos, many=True)

        return response.Response(serializer.data)

    def put(self, request, id=None):
        todo = get_object_or_404(Todos, id=id)
        serializer = self.serializer_class(todo, data=request.data)
        if serializer.is_valid():
            serializer.save(owner=self.request.user)
            return response.Response(serializer.data, status=status.HTTP_200_OK)

        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id=None):

        todo = get_object_or_404(Todos, id=id)

        todo.delete()

        return response.Response({"message": "object delete successfull"}, status=status.HTTP_204_NO_CONTENT)
