from ..models import User
from rest_framework import generics, status
from ..serializers import RegisterSerializer
from rest_framework.response import Response
from ..utils import Util
from rest_framework import status
from ..permissions import IsAdmin


class RegisterView(generics.GenericAPIView):
 
    serializer_class = RegisterSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data

        user = User.objects.get(email=user_data['email'])
        user_data = serializer.data
        otp = Util.generate_otp(6)
        user.otp = otp
        user.save()

        absurl = str(otp)
        email_body = 'Hi '+user.username+' Use OTP below to verify ypur email \n'+ absurl
        data = {'email_body': email_body, 'to_email': user.email, 'email_subject': 'verify your email'}
        Util.send_email(data)
        return Response(user_data, status=status.HTTP_201_CREATED)
 
   
class RegisterAdminView(generics.GenericAPIView):

    serializer_class = RegisterSerializer
    Permission_classes = [IsAdmin]

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data

        user = User.objects.get(email=user_data['email'])
        user_data = serializer.data
        otp = Util.generate_otp(6)
        user.otp = otp
        user.is_staff = True
        user.save()
        return Response(user_data, status=status.HTTP_201_CREATED)
