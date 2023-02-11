from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from authentification.serializer import RegisterSerilizer
from rest_framework import response, status

# Create your views here.


class ResgisterAPIView(GenericAPIView):

    serializer_class = RegisterSerilizer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)

        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def get(self, id):
    #     pass

    # def put(self, request):
    #     pass

    # def delete(self, id):
    #     pass
