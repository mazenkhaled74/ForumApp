from django.urls import path
from .views import QuestionListCreateAPIView, AnswerQuestionAPIView, UpVoteAPIView,DownVoteAPIView,AcceptAnswerAPIView, CommentAPIView,QuestionDetailAPIView

urlpatterns = [
    path('questions', QuestionListCreateAPIView.as_view(), name='questions'),
    path('questions/<int:pk>', QuestionDetailAPIView.as_view(), name='question_detail'),
    path('answer/<int:pk>', AnswerQuestionAPIView.as_view(), name='answer'),
    path('answer/upvote/<int:pk>', UpVoteAPIView.as_view(), name='upvote'),
    path('answer/downvote/<int:pk>', DownVoteAPIView.as_view(), name='downvote'),
    path('answer/accept/<int:pk>', AcceptAnswerAPIView.as_view(), name='accept'),
    path('answer/comment/<int:pk>', CommentAPIView.as_view(), name='comment'),
]
