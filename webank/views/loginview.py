from rest_framework import status
from ..serializers import LoginSerializer, LogoutSerializer
from rest_framework.response import Response
from django.contrib.auth import authenticate, logout
from rest_framework import status, permissions, generics
from rest_framework.generics import GenericAPIView
from rest_framework.authtoken.models import Token


class LoginView(GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = LoginSerializer
    
    def post(self, request):
        email = request.data.get('email', '')
        password = request.data.get('password', '')
        if email is None or password is None:
            return Response(data={'invalid_credentials': 'Please provide both email and password'}, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=email, password=password)
        if not user:
            return Response(data={'invalid_credentials': 'Ensure both email and password are correct and you have verified your account'}, status=status.HTTP_400_BAD_REQUEST)
        if not user.is_verified:
            return Response(data={'invalid_credentials': 'Please verify your account'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(user)
        token, _ = Token.objects.get_or_create(user=user)
        return Response(data={'token': token.key,}, status=status.HTTP_200_OK)
    
class LogoutView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    
    def get(self, request):
        logout(request)
        return Response({"success": "You have successfully logged out"}, status=status.HTTP_200_OK)