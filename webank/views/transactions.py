from ..models import TransactionHistory, User
from rest_framework import generics, status
from ..serializers import  TransactionsHistory
from rest_framework.response import Response
from rest_framework import status
from ..permissions import IsAdmin
from rest_framework.permissions import IsAuthenticated


class Transactions(generics.GenericAPIView):
    permission_classes = [IsAdmin]
    
    def get(self, request):
        queryset = TransactionHistory.objects.all()
        serializer = TransactionsHistory(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class Transaction(generics.GenericAPIView):
    permission_class = [IsAuthenticated]
    
    def get(self, request):
        user_id  = User.object.get(email='email')
        try:
            transaction = TransactionHistory.objects.filter(user=user_id)
            serializer = TransactionsHistory(transaction)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({'Error': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)