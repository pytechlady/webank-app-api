from ..models import TransactionHistory, User
from rest_framework import generics, status
from ..serializers import  TransactionSerializer
from rest_framework.response import Response
from rest_framework import status
from ..permissions import IsAdmin



class Transactions(generics.GenericAPIView):
    permission_classes = [IsAdmin]
    
    def get(self, request):
        queryset = TransactionHistory.objects.all()
        serializer = TransactionSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class Transaction(generics.GenericAPIView):
    permission_class = [IsAdmin]
    
    def get(self, request, pk):
        try:
            queryset = TransactionHistory.objects.get(pk=pk)
            serializers = TransactionSerializer(queryset)
            return Response(serializers.data, status=status.HTTP_200_OK)
        except:
            return Response({'Error': 'Transaction does not exist'}, status=status.HTTP_400_BAD_REQUEST)