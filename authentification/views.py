from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from authentification.serializer import RegisterSerilizer, LoginSerilizer
from rest_framework import response, status, permissions
from django.contrib.auth import authenticate

# Create your views here.


class AuthUserAPIView(GenericAPIView):

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = RegisterSerilizer

    def get(self, request):

        user = request.user

        serializer = self.serializer_class(user)
        return response.Response({'user': serializer.data})


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


class LoginAPIView(GenericAPIView):

    serializer_class = LoginSerilizer

    def post(self, request):
        email = request.data.get("email", None)
        password = request.data.get("password", None)

        user = authenticate(username=email, password=password)

        if user:
            serializer = self.serializer_class(user)
            return response.Response(serializer.data, status=status.HTTP_200_OK)

        return response.Response({"message": "invalid credential, try again"}, status=status.HTTP_401_UNAUTHORIZED)
