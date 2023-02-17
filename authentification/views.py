from rest_framework.generics import GenericAPIView
from authentification.serializer import RegisterSerilizer, LoginSerilizer
from rest_framework import response, status, permissions
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password, check_password
import random
import jwt
from datetime import datetime, timedelta
from django.conf import settings
from authentification.models import User
from helpers.utils import recover_email, check_token

# Create your views here.


class AuthUserAPIView(GenericAPIView):

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = RegisterSerilizer

    def get(self, request):

        user = request.user

        serializer = self.serializer_class(user)
        return response.Response({'user': serializer.data}, status=status.HTTP_200_OK)


class ResgisterAPIView(GenericAPIView):
    permission_classes = ()
    authentication_classes = ()
    serializer_class = RegisterSerilizer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)

        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(GenericAPIView):

    permission_classes = ()
    authentication_classes = ()
    serializer_class = LoginSerilizer

    def post(self, request):
        email = request.data.get("email", None)
        password = request.data.get("password", None)

        user = authenticate(username=email, password=password)

        if user:
            serializer = self.serializer_class(user)
            return response.Response(serializer.data, status=status.HTTP_200_OK)

        return response.Response({"message": "invalid credential, try again"}, status=status.HTTP_401_UNAUTHORIZED)


class EmailSign(GenericAPIView):
    permission_classes = ()
    authentication_classes = ()

    def post(self, request):
        email = request.data.get("email", None)
        user = User.objects.filter(email=email).first()

        if user:
            uncripted_code = random.randrange(1000, 9999)
            recover_email(email=user.email, uncripted_code=uncripted_code)
            code = make_password(str(uncripted_code))
            token = jwt.encode(
                {
                    'username': user.username,
                    'email': user.email,
                    'user_id': user.id,
                    'code': code,
                    'exp': datetime.utcnow()+timedelta(hours=1)
                }, settings.SECRET_KEY2, algorithm='HS256')

            return response.Response({
                "token": token,
                "message": "Code de vérification envoyé",
                "user_id": user.id
            }, status=status.HTTP_200_OK)

        return response.Response({"message": "The user does not exist"}, status=status.HTTP_401_UNAUTHORIZED)


class CodeVerification(GenericAPIView):

    permission_classes = ()
    authentication_classes = ()
    serializer_class = LoginSerilizer

    def post(self, request):

        payload = check_token(request)
        code = request.data.get("code", None)
        if check_password(code, payload['code']):
            user_id = payload['user_id']
            user = User.objects.get(id=user_id)
            if user:
                serializer = self.serializer_class(user)
                return response.Response(serializer.data, status=status.HTTP_200_OK)

            return response.Response({"message": "The user does not exist, try again."}, status=status.HTTP_401_UNAUTHORIZED)
        return response.Response({"message": "invalid code, try again."}, status=status.HTTP_400_BAD_REQUEST)
