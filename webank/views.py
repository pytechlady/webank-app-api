from .models import User
from rest_framework import generics, status
from .serializers import RegisterSerializer, EmailVerificationSerializer
from rest_framework.response import Response
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import authenticate, logout
from rest_framework import status, permissions
from rest_framework.generics import GenericAPIView
from rest_framework.authtoken.models import Token
# from .serializers import LoginSerializer
from django.core.exceptions import ObjectDoesNotExist


    
class RegisterView(generics.GenericAPIView):
    
    serializer_class = RegisterSerializer
    
    def post(self, request):
        user=request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        
        user = User.object.get(email=user_data['email'])
        user_data = serializer.data
        otp = Util.generate_otp(6)
        user.otp = otp
        user.save()
        current_site = get_current_site(request).domain
    
       
        absurl = 'http://'+current_site+'?token='+str(otp)
        email_body = 'Hi '+user.username+' Use link below to verify ypur email \n'+ absurl
        data = {'email_body':email_body, 'to_email':user.email, 'email_subject': 'verify your email'}
        Util.send_email(data)
        
        return Response(user_data, status=status.HTTP_201_CREATED)

class VerifyEmail(generics.GenericAPIView):
    serializer_class = EmailVerificationSerializer
    
    def post(self, request):
        data = request.data
        otp = data.get('otp', '')
        email = data.get('email', '')
        if otp is None or email is None:
            return Response(data=dict(invalid_input="Please provide both otp and email"), status=status.HTTP_400_BAD_REQUEST)
        get_user = User.object.filter(email=email)
        if not get_user.exists():
            return Response(data=dict(invalid_email = "please provide a valid registered email"), status=status.HTTP_400_BAD_REQUEST )
        user = get_user[0] 
        if user.otp != otp:
            return Response(data=dict(invalid_otp = "please provide a valid otp code"), status=status.HTTP_400_BAD_REQUEST)
        user.is_verified = True
       
        user.save()
        return Response(data={
                "verified status":"Your account has been successfully verified"
            }, status=status.HTTP_200_OK)