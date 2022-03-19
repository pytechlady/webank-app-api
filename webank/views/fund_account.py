from ..models import AccountManager, TransactionHistory, User, Balance
from rest_framework import generics, permissions, status, viewsets
from ..serializers import BalanceSerializer
from rest_framework.response import Response
from rest_framework import status
from ..utils import Util
from ..permissions import IsAdmin


class CreditBalance(generics.GenericAPIView):
    serializer_class = BalanceSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdmin]
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            customer_account = serializer.validated_data.get('account_number')
            account = AccountManager.objects.filter(account_number=customer_account)[0]
            user = User.objects.get(email=account.user_id)
            balance = Balance.objects.filter(customer=user).first()
            if balance and user.is_verified:
                credit_or_debit = serializer.validated_data.get('amount')
                balance.account_balance += credit_or_debit
                balance.save()
                transaction_type = "Credit"
                transaction = TransactionHistory.objects.create(
                    user_id = user,
                    account_id = AccountManager.objects.filter(user_id = user)[0],
                    transaction_type = transaction_type,
                    transaction_amount = credit_or_debit,
                    balance_id = Balance.objects.filter(customer=user)[0], 
                    current_balance = balance.account_balance,
                )
                transaction.save()
                

                absurl = str(credit_or_debit)
                email_body = 'Hi '+user.username+' your account has been credited with \n#'+ absurl+ 'your current balnace is #' + str(transaction.current_balance)
                data = {'email_body': email_body, 'to_email': user.email, 'email_subject': 'Credit alert'}
                Util.send_email(data)
                return Response({"success": f'account funded sucessfully with {credit_or_debit}'}, status=status.HTTP_201_CREATED)
            elif not balance and user.is_verified:
                account = AccountManager.objects.filter(account_number=customer_account)[0]
                balance = Balance.objects.create(
                    customer = user,
                    customer_account = account,
                    account_balance = 0
                )
                credit_or_debit = serializer.validated_data.get('amount')
                balance.account_balance += credit_or_debit
                balance.save()
                transaction_type = "Credit"
                transaction = TransactionHistory.objects.create(
                    user_id = user,
                    account_id = AccountManager.objects.filter(user_id = user)[0],
                    transaction_type = transaction_type,
                    transaction_amount = credit_or_debit,
                    balance_id = Balance.objects.filter(customer=user)[0], 
                    current_balance = balance.account_balance,
                )
                transaction.save()

                absurl = str(credit_or_debit)
                email_body = 'Hi '+user.username+' your account has been credited with \n#'+ absurl+ ' your current balance is #'+ str(transaction.current_balance)
                data = {'email_body': email_body, 'to_email': user.email, 'email_subject': 'Credit alert'}
                Util.send_email(data)
                return Response({"success": f'account funded sucessfully with {credit_or_debit}'}, status=status.HTTP_201_CREATED)
            else:
                return Response({"error": "Contact Administration"}, status=status.HTTP_403_FORBIDDEN)
        return Response({"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
class DebitBalance(generics.GenericAPIView):
    serializer_class = BalanceSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdmin]
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            customer_account = serializer.validated_data.get('account_number')
            account = AccountManager.objects.filter(account_number=customer_account)[0]
            user = User.objects.get(email=account.user_id)
            balance = Balance.objects.filter(customer=user).first()
            if balance and user.is_verified:
                credit_or_debit = serializer.validated_data.get('amount')
                
                if balance.account_balance >= credit_or_debit:
                    balance.account_balance -= credit_or_debit
                    balance.save()
                    transaction_type = "Debit"
                    transaction = TransactionHistory.objects.create(
                        user_id = user,
                        account_id = AccountManager.objects.filter(user_id = user)[0],
                        transaction_type = transaction_type,
                        transaction_amount = credit_or_debit,
                        balance_id = Balance.objects.filter(customer=user)[0],
                        current_balance = balance.account_balance,
                    )
                    transaction.save()
                    
                    
                    absurl = str(credit_or_debit)
                    email_body = 'Hi '+user.username+' your account has been debited with \n#'+ absurl+ ' your current balance is #' + str(transaction.current_balance)
                    data = {'email_body': email_body, 'to_email': user.email, 'email_subject': 'Debit alert'}
                    Util.send_email(data)
                    return Response({"success": f'account debited sucessfully with {credit_or_debit}'}, status=status.HTTP_201_CREATED)
                else:
                    balance.account_balance = balance.account_balance
                    balance.save()
                    return Response({'Error': f'Insuffient funds. Your account balance is {balance.account_balance}'}, status=status.HTTP_402_PAYMENT_REQUIRED)
                    
            elif user.is_verified:
                account = AccountManager.objects.filter(account_number=customer_account)[0]
                balance = Balance.objects.create(
                    customer = user,
                    customer_account = account,
                    account_balance = 0
                )
                credit_or_debit = serializer.validated_data.get('amount')
                balance.account_balance = balance.account_balance
                balance.save()
                
                return Response({"Error": f'Insufficient fund, kindly credit your account'}, status=status.HTTP_402_PAYMENT_REQUIRED)
            else:
                return Response({"error": "Contact Administration"})
        return Response({"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)