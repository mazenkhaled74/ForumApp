from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from auth_manager.serializers import UserSerializer
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from auth_manager.models import CustomUser

class RegisterView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data= request.data)
        if serializer.is_valid():
            password = serializer.validated_data.get('password')
            hashedPassword = make_password(password)
            serializer.validated_data['password'] = hashedPassword
            serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    
class LogInView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        if username is None or password is None:
            return Response({'error': 'Password and Username are required'})
        
        user = authenticate(username= username, password= password)
        if user is not None:
            return Response("Loged in successfully", status= status.HTTP_200_OK)
        return Response("Invalid Credentials", status=status.HTTP_401_UNAUTHORIZED)
    
class GetReputationAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        user = get_object_or_404(CustomUser, pk=pk)
        return Response({'reputation': user.reputation}, status=status.HTTP_200_OK)