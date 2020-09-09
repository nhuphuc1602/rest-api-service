from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from rest_framework import routers
from qa_service import views
from django.urls import path
from knox import views as knox_views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.views.generic import TemplateView
from rest_framework.authtoken import views as authtoken_views

router = routers.SimpleRouter()
router.register(r'questions', views.QAAPIView, basename='Questions')
router.register(r'answers', views.AnswerAPIView, basename='Answers')
router.register(r'questions', views.QARudView, basename='Questions')
router.register(r'answers', views.AnswerRudView, basename='Answers')
router.register(r'tags', views.TagView, basename='Tags')

urlpatterns = [
    
    path(r'', views.home_view),
    path(r'readme/', views.readme_view),
    url(r'^admin/', admin.site.urls), 
    url('^api/', include(router.urls)),
    url(r'accounts/', include('rest_registration.api.urls')),
    url(r'user/', views.ListUsers.as_view(), name = 'home'),
    url(r'^api/token/$', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    url(r'^api/token/refresh/$', TokenRefreshView.as_view(), name='token_refresh'),
    path('api_generate_token', authtoken_views.obtain_auth_token),
    path('vote/', views.QuestionViewSet.as_view({'get': 'list'}), name='vote'),
    path('rest-auth/', include('rest_auth.urls')),
    path('api/register/', views.RegisterAPI.as_view(), name='register'),

]