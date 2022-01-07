from ..models import User
from rest_framework import generics, status
from ..serializers import AccountSerializer
from rest_framework.response import Response
from rest_framework import status
from ..permissions import IsAdmin


class DeleteAcount(generics.GenericAPIView):
    permission_classes = [IsAdmin]
    serializer_class = AccountSerializer
    queryset = User.object.all()
    
    def delete(self, request, pk):
        try:
            user_account = User.object.get(pk = pk)
            user_account.delete()
            return Response({'data':"user successfully deleted"}, status=status.HTTP_200_OK) 
        except Exception as error:
            return Response({"error": error}, status= status.HTTP_400_BAD_REQUEST) 
        
class DeactiveAccount(generics.GenericAPIView):
    permission_classes = [IsAdmin]
    serializer_class = AccountSerializer
    
    queryset = User.object.all()
    
    def post(self, request, pk):
        try:
            user_account = User.object.get(pk = pk)
            user_account.is_verified = False
            user_account.save()
            return Response({'data':"user successfully deactivated"}, status=status.HTTP_200_OK) 
        except Exception as error:
            return Response({"error": error}, status= status.HTTP_400_BAD_REQUEST)
        
class ActivateAccount(generics.GenericAPIView):
    permission_classes = [IsAdmin]
    serializer_class = AccountSerializer
    
    queryset = User.object.all()
    
    def post(self, request, pk):
        try:
            user_account = User.object.get(pk = pk)
            user_account.is_verified = True
            user_account.save()
            return Response({'data':"user successfully activated"}, status=status.HTTP_200_OK) 
        except Exception as error:
            return Response({"error": error}, status= status.HTTP_400_BAD_REQUEST)