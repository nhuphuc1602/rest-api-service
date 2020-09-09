from rest_framework import serializers

from qa_service.models import Question, Answer, Tag

from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = [
            'name'
           
        ]


class QuestionSerializer(serializers.ModelSerializer):
    author_text = serializers.CharField( read_only=True)
    class Meta:
        model = Question
        fields = [
            'pk',
            'question',
            'author',
            'author_text',
            'updated',
            'created',
            'num_vote_up',
            'num_vote_down',
            'tags',
            'status',   
        ]
    

class AnswerSerializer(serializers.ModelSerializer):
    question_text = serializers.CharField(source='question.question', read_only=True)
    author_text = serializers.CharField(source='author.username', read_only=True)
    status = serializers.BooleanField(source='question.status')
    class Meta:
        model = Answer
        fields = [
            'pk',
            'question_text',
            'question',
            'author',
            'author_text',
            'answer',
            'updated',
            'num_vote_up',
            'num_vote_down',
            'status',
        ]
    


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])

        return user


