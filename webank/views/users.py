from ..models import User
from rest_framework import generics, status
from ..serializers import  RegisterSerializer
from rest_framework.response import Response
from rest_framework import status
from ..permissions import IsAdmin



class Users(generics.GenericAPIView):
    permission_classes = [IsAdmin]
    
    def get(self, request):
        queryset = User.object.all()
        serializer = RegisterSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class OneUser(generics.GenericAPIView):
    permission_classes = [IsAdmin]
    
    def get(self, request):
        try:
            queryset = User.object.get()
            serializer = RegisterSerializer(queryset)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({"Error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)