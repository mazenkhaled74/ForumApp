from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Question, CustomUser, Answer
from .serializers import GetQuestionSerializer, CreateQuestionSerializer, CreateAnswerSerializer, CommentSerializer
from django.shortcuts import get_object_or_404
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from moderation.permissions import IsBlockedUser
class QuestionListCreateAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsBlockedUser]

    def get(self, request, *args, **kwargs):
        questions = Question.objects.all()
        serializer = GetQuestionSerializer(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = CreateQuestionSerializer(data= request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user= request.user)
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

class QuestionDetailAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsBlockedUser]

    def get(self, request, pk):
        question = get_object_or_404(Question, pk=pk)
        serializer = GetQuestionSerializer(question)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class AnswerQuestionAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsBlockedUser]

    def patch(self, request, pk):
        question = get_object_or_404(Question, pk=pk)
        serializer = CreateAnswerSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            serializer.save(question=question)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpVoteAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsBlockedUser]

    def patch(self, request, pk):
        answer = get_object_or_404(Answer, pk= pk)
        if request.user != answer.user:
            answer.upvotes += 1
            answer.save()
            return Response({'upvotes': answer.upvotes}, status=status.HTTP_200_OK)
        return Response({'error': 'user cannot vote his own answer'}, status=status.HTTP_403_FORBIDDEN)
    
class DownVoteAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsBlockedUser]

    def patch(self, request, pk):
        answer = get_object_or_404(Answer, pk= pk)
        if request.user != answer.user:
            answer.downvotes += 1
            answer.save()
            return Response({'downvotes': answer.downvotes}, status=status.HTTP_200_OK)
        return Response({'error': 'user cannot vote his own answer'}, status=status.HTTP_403_FORBIDDEN)

class AcceptAnswerAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsBlockedUser]

    def patch(self, request, pk):
        answer = get_object_or_404(Answer, pk= pk)
        if request.user == answer.question.user:
            answer.accepted = True
            answer.save()
            return Response({'answer status': answer.accepted}, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_403_FORBIDDEN)

class CommentAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsBlockedUser]

    def post(self, request, pk):
        answer = get_object_or_404(Answer, pk=pk)
        serializer = CommentSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(answer=answer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    