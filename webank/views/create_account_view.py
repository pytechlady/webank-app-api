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
            account_type = AccountManager.objects.values_list('account_type', flat=True).distinct()
            account_number = Util.generate_account_number()
            phone_number = serializer.validated_data.get('phone_number')
            gender = AccountManager.objects.values_list('gender', flat=True).distinct()
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
                
                return Response({"success": f"account succesfully created, your account number is {account.account_number}"}, status=status.HTTP_206_PARTIAL_CONTENT)
                
            except:
                return Response({'error': 'You already have an account'}, status=status.HTTP_400_BAD_REQUEST)
            
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)