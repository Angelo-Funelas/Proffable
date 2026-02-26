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

urlpatterns = [
    path("token/", CustomTokenObtainPairView.as_view()),
    path("token/refresh/", TokenRefreshView.as_view()),
    path("register/", register_user),
    path("me/", me),
    path('', include(router.urls)),
]