from ..models import User
from rest_framework import generics, status
from ..serializers import  RegisterSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework import status
from ..permissions import IsAdmin



class Users(generics.GenericAPIView):
    permission_classes = [IsAdmin]
    
    def get(self, request):
        queryset = User.objects.all()
        serializer = RegisterSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class OneUser(generics.GenericAPIView):
    permission_classes = [IsAdmin]
    
    def get(self, request, pk):
        try:
            queryset = User.objects.get(pk=pk)
            serializers = RegisterSerializer(queryset)
            return Response(serializers.data, status=status.HTTP_200_OK)
        except:
            return Response({"Error": "User does not exist"}, status=status.HTTP_400_BAD_REQUEST)

