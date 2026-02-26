from django.urls import path, include
from rest_framework.routers import DefaultRouter

from professors.views import ProfessorViewSet, ReviewViewSet

router = DefaultRouter()
router.register(r"professors",ProfessorViewSet)
router.register(r"reviews",ReviewViewSet)

#include logic for jwt 
from .serializers import CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from .views import me
from .views import register_user
from .views import google_login

urlpatterns = [
    path("token/", CustomTokenObtainPairView.as_view()),
    path("token/refresh/", TokenRefreshView.as_view()),
    path("register/", register_user),
    path("google-login", google_login),
    path("me/", me),
    path('', include(router.urls)),
]