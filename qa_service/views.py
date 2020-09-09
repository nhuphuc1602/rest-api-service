from qa_service.models import Question, Answer, Tag
from .serializers import QuestionSerializer, UserSerializer, AnswerSerializer, TagSerializer, RegisterSerializer

from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse, HttpResponseRedirect

from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, serializers, viewsets, generics, mixins, authentication, status, viewsets
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.authentication import BasicAuthentication, TokenAuthentication

from vote.views import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class QAAPIView(mixins.CreateModelMixin,  generics.ListAPIView, viewsets.GenericViewSet):
    lookup_field = 'pk'
    serializer_class = QuestionSerializer
    #queryset = Answer.objects.all()
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get_queryset(self):
        qs = Question.objects.all()
        query = self.request.GET.get("q")
        if query is not None:
            qs = qs.filter(Q(question__icontains= query)|Q(author__icontains= query)).distinct()
        return Question.objects.order_by('pk')

    def perfom_create(self, serializer):
        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)



class AnswerRudView(generics.RetrieveUpdateDestroyAPIView, viewsets.GenericViewSet):
    # lookup_field = 'pk'
    serializer_class = AnswerSerializer
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    #queryset = Answer.objects.all()

    def get_queryset(self):
        return Answer.objects.all()


class AnswerAPIView(mixins.CreateModelMixin,  generics.ListAPIView, viewsets.GenericViewSet,):
    # lookup_field = 'pk'
    serializer_class = AnswerSerializer
    #queryset = Answer.objects.all()
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        qs = Answer.objects.all()
        query = self.request.GET.get("a")
        if query is not None:
            qs = qs.filter(Q(answer__icontains= query)|Q(author__icontains= query)).distinct()
        return Answer.objects.all().filter(question__status = True)#order_by('pk')

    def perfom_create(self, serializer):
        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class QARudView(generics.RetrieveUpdateDestroyAPIView, viewsets.GenericViewSet):
    lookup_field = 'pk'
    serializer_class = QuestionSerializer
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    #queryset = Answer.objects.all()

    def get_queryset(self):
        return Question.objects.all()


class TagView(mixins.CreateModelMixin,  generics.ListAPIView, viewsets.GenericViewSet,):
    # lookup_field = 'pk'
    serializer_class = TagSerializer
    #queryset = Answer.objects.all()
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        qs = Tag.objects.all()
        query = self.request.GET.get("a")
        if query is not None:
            qs = qs.filter(Q(answer__icontains= query)|Q(author__icontains= query)).distinct()
        return Tag.objects.all()

    def perfom_create(self, serializer):
        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ListUsers(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        usernames = [user.username for user in User.objects.all()]
        return Response(usernames)

class RegisterAPI(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer
    def get(self, request, format=None):
        return Response()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })

class QuestionViewSet(viewsets.ModelViewSet, VoteMixin):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

def home_view(request):
    return render(request, 'home.html')

def readme_view(request):
    return render(request, 'readme.html')
