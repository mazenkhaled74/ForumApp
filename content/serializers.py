from rest_framework import serializers
from .models import Question, Category, Tag, Comment, Answer, CustomUser

class CreateQuestionSerializer(serializers.ModelSerializer):
    categories = serializers.SlugRelatedField(slug_field='name', queryset= Category.objects.all(), many=True)
    tags = serializers.SlugRelatedField(slug_field='name', queryset= Tag.objects.all(), many=True)
    class Meta:
        model = Question
        fields = ['id', 'title', 'content', 'created_at' ,'categories', 'tags']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class GetCommentSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', queryset=CustomUser.objects.all())

    class Meta:
        model = Comment
        fields = ['id', 'user', 'content', 'created_at']

class AnswerSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', queryset=CustomUser.objects.all())
    comments = GetCommentSerializer(many= True, read_only=True, source = 'comment_set')
    class Meta:
        model = Answer
        fields = ['id', 'user', 'content', 'upvotes', 'downvotes', 'accepted','comments' ,'created_at']

class CreateAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'content', 'created_at']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class GetQuestionSerializer(serializers.ModelSerializer):
    categories = serializers.SlugRelatedField(slug_field='name', queryset= Category.objects.all(), many=True)
    tags = serializers.SlugRelatedField(slug_field='name', queryset= Tag.objects.all(), many=True)
    user = serializers.SlugRelatedField(slug_field='username', queryset=CustomUser.objects.all())
    answers = AnswerSerializer(many=True, read_only=True, source='answer_set')

    class Meta:
        model = Question
        fields = ['id', 'user', 'title', 'content', 'created_at', 'categories', 'tags',  'answers']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_at']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    