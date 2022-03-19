from ..models import User
from rest_framework import generics, status
from ..serializers import EmailVerificationSerializer
from rest_framework.response import Response
from rest_framework import status




class VerifyEmail(generics.GenericAPIView):
    serializer_class = EmailVerificationSerializer
    
    def post(self, request):
        data = request.data
        otp = data.get('otp', '')
        email = data.get('email', '')
        if otp is None or email is None:
            return Response(data=dict(invalid_input="Please provide both otp and email"), status=status.HTTP_400_BAD_REQUEST)
        get_user = User.objects.filter(email=email)
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