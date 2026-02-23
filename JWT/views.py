from http.client import responses

from .models import User
from .serializers import UserSerializers,RegisterSerializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authentication import authenticate

class RegisterView(APIView):
    def post(self,request):
        serializer =RegisterSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.save()
        response={
            'status':status.HTTP_200_OK,
            'message':"Siz ro'yxatdan o'tdingiz",
            'data':user.username
        }
        return Response(response)


class Login(APIView):
    def post(self,request):
        username=self.request.data.get('username')
        password=self.request.data.get('password')

        user=authenticate(username=username,password=password)

        if not user:
            return Response({'error':'Parol yoki username xato'})
        refresh_token=RefreshToken.for_user(user=user)

        response={
            'status':status.HTTP_200_OK,
            'message':'login qildiz',
            'refresh_token':str(refresh_token),
            'access':str(refresh_token.access_token)
        }
        return Response(response)

