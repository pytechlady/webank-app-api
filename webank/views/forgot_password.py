from ..models import User
from rest_framework import generics
from ..serializers import ForgotPasswordSerializer, PasswordResetSerializer
from rest_framework.response import Response
from ..utils import Util
from django.core.exceptions import ObjectDoesNotExist


class ForgotPasswordView(generics.GenericAPIView):
    serializer_class = ForgotPasswordSerializer
    def post(self, request):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
            
        except ObjectDoesNotExist:
            return Response({"message":"User does not exist"}, status=404)
        OTP=Util.generate_otp(6)
        user.otp = OTP
        email = user.email
        user.save()
        if user.is_active == True:  
            email_body = 'Hi '+user.username+'Here is the Otp code to reset your password \n' + str(OTP)
            data = {'email_body':email_body, 'to_email':user.email, 'email_subject': 'verify your email'}
            Util.send_email(data)
            return Response({
                "message": "success",
                "errors": None
            }, status=200)
            
class PasswordReset(generics.GenericAPIView):
    serializer_class=PasswordResetSerializer

    def put(self, request):
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        otp = serializer.data.get('otp')
        password = request.data.get('password')
        confirm_password =request.data.get('confirm_password')
        try:
            user = User.objects.get(email=email)
        except ObjectDoesNotExist:
            return Response({"message":"User does not exist"}, status=404)
        if password == confirm_password:
            keygen=user.otp
            OTP=keygen
            if otp != OTP:  
                return Response({
                "message": "Failure",
                "data": None,
                "errors": {
                    'otp_code': "OTP does not match or expired"
                }
            }, status=400)
            user.set_password(password)
            user.save()
            return Response({
                "message": 'success! Password reset successful' ,
                "data": {
                    "otp": None
                },
                "errors": None
            }, status=200)
        else:
            return Response({"message":"Failure","data":None,"errors":{
                "passwords": "The two Passwords must be the same"
            }},status=400)