from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from auth_manager.models import CustomUser
from django.shortcuts import get_object_or_404

class BlockUserAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def post(self, request, pk):
        user = get_object_or_404(CustomUser, pk= pk)
        user.blocked = True
        user.save()
        return Response({"status" : "User blocked"}, status= status.HTTP_200_OK)
    

class UnblockUserAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def post(self, request, pk):
        user = get_object_or_404(CustomUser, pk= pk)
        user.blocked = False
        user.save()
        return Response({"status" : "User unblocked"}, status= status.HTTP_200_OK)
    

