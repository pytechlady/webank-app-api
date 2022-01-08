from ..models import AccountManager, User, Balance
from rest_framework import generics, status
from ..serializers import BalanceSerializer
from rest_framework.response import Response
from rest_framework import status
from ..utils import Util
from ..permissions import IsAdmin


class CreditBalance(generics.GenericAPIView):
    serializer_class = BalanceSerializer
    queryset = User.object.all()
    permission_classes = [IsAdmin]
    
    def post(self, request, pk):
        print(request.data)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.object.get(pk = pk)
        balance = Balance.objects.filter(customer=user).first()
        if balance:
            credit_or_debit = serializer.validated_data.get('account_balance')
            balance.account_balance += credit_or_debit
            balance.save()

            absurl = str(credit_or_debit)
            email_body = 'Hi '+user.username+' your account has been credited with \n'+ absurl
            data = {'email_body': email_body, 'to_email': user.email, 'email_subject': 'Credit alert'}
            Util.send_email(data)
            return Response({"success": f'account funded sucessfully with {credit_or_debit}'}, status=status.HTTP_201_CREATED)
        else:
            account = AccountManager.objects.get(user_id = user)
            balance = Balance.objects.create(
                customer = user,
                customer_account = account,
                account_balance = 0
            )
            credit_or_debit = serializer.validated_data.get('account_balance')
            balance.account_balance += credit_or_debit
            balance.save()

            absurl = str(credit_or_debit)
            email_body = 'Hi '+user.username+' your account has been credited with \n'+ absurl
            data = {'email_body': email_body, 'to_email': user.email, 'email_subject': 'Credit alert'}
            Util.send_email(data)
            return Response({"success": f'account funded sucessfully with {credit_or_debit}'}, status=status.HTTP_201_CREATED)
        
class DebitBalance(generics.GenericAPIView):
    serializer_class = BalanceSerializer
    queryset = User.object.all()
    permission_classes = [IsAdmin]
    
    def post(self, request, pk):
        print(request.data)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.object.get(pk = pk)
        balance = Balance.objects.filter(customer=user).first()
        if balance:
            credit_or_debit = serializer.validated_data.get('account_balance')
            if balance.account_balance >= credit_or_debit:
                balance.account_balance -= credit_or_debit
                balance.save()
                absurl = str(credit_or_debit)
                email_body = 'Hi '+user.username+' your account has been debited with \n'+ absurl
                data = {'email_body': email_body, 'to_email': user.email, 'email_subject': 'Debit alert'}
                Util.send_email(data)
                return Response({"success": f'account debited sucessfully with {credit_or_debit}'}, status=status.HTTP_201_CREATED)
            else:
                balance.account_balance = balance.account_balance
                balance.save()
                return Response({'Error': f'Insuffient funds. Your account balance is {balance.account_balance}'}, status=status.HTTP_400_BAD_REQUEST)
                
        else:
            account = AccountManager.objects.get(user_id = user)
            balance = Balance.objects.create(
                customer = user,
                customer_account = account,
                account_balance = 0
            )
            credit_or_debit = serializer.validated_data.get('account_balance')
            balance.account_balance = balance.account_balance
            balance.save()
            
            return Response({"Error": f'Insufficient fund, kindly credit your account'}, status=status.HTTP_402_PAYMENT_REQUIRED)
     
    
