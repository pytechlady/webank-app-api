from ..models import AccountManager
from rest_framework import generics, status
from ..serializers import AccountSerializer
from rest_framework.response import Response
from ..utils import Util
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


    
class AccountView(generics.GenericAPIView):
    
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user_id  = request.user
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            fullname =serializer.validated_data.get('fullname')
            account_type = serializer.validated_data.get('account_type')
            account_number = Util.generate_account_number()
            phone_number = serializer.validated_data.get('phone_number')
            gender = serializer.validated_data.get('gender')
            occupation = serializer.validated_data.get('occupation')
            address =serializer.validated_data.get('address')
            try:
                account = AccountManager.objects.create(
                    user_id = user_id,
                    fullname = fullname,
                    account_type = account_type,
                    account_number = account_number,
                    phone_number = phone_number,
                    gender = gender,
                    occupation = occupation,
                    address = address,
                )

                absurl = str(account_number)
                email_body = 'Hi '+fullname+', your account has been succesfully created.\nYour account number is '+ absurl
                data = {'email_body': email_body, 'to_email': user_id, 'email_subject': 'Account Created'}
                Util.send_email(data)
                
                return Response({"success": f"account succesfully created, your account number is {account.account_number}"}, status=status.HTTP_206_PARTIAL_CONTENT)
                
            except:
                return Response({'error': 'You already have an account'}, status=status.HTTP_400_BAD_REQUEST)
            
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)