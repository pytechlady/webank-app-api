from ..models import AccountManager
from rest_framework import generics, status
from ..serializers import AccountViewSerializer
from rest_framework.response import Response
from ..utils import Util
from rest_framework import status
from ..permissions import IsAdmin
from rest_framework.permissions import IsAuthenticated



class Accounts(generics.GenericAPIView):
    permission_classes = [IsAdmin]
    
    def get(self, request):
        queryset = AccountManager.objects.all()
        serializer = AccountViewSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class Account(generics.GenericAPIView):
    permission_classes = [IsAdmin]
    
    def get(self, request, pk):
        try:
            queryset = AccountManager.objects.get(pk=pk)
            serializer = AccountViewSerializer(queryset)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({"Error": "Account does not exist"}, status=status.HTTP_404_NOT_FOUND)
            
     