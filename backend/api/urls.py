from django.urls import path, include
from rest_framework.routers import DefaultRouter

from professors.views import ProfessorViewSet, ReviewViewSet, InstitutionViewSet, CourseViewSet, ReviewReportViewSet
from professors.views import TagViewSet, FavoriteProfViewset
router = DefaultRouter()
router.register(r"professors",ProfessorViewSet)
router.register(r"reviews",ReviewViewSet)
router.register(r"review-reports", ReviewReportViewSet)
router.register(r"institutions", InstitutionViewSet)
router.register(r"courses", CourseViewSet)
router.register(r"tags",TagViewSet)
router.register(r"favorite-prof", FavoriteProfViewset)


#include logic for jwt 
from .serializers import CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from .views import me
from .views import register_user
from .views import google_login
from .views import LoginView
from .views import update_profile
from .views import delete_profile

urlpatterns = [
    path("token/", LoginView.as_view()),
    path("token/refresh/", TokenRefreshView.as_view()),
    path("register/", register_user),
    path("google-login/", google_login),
    path("me/", me),
    path("me/update/", update_profile),
    path("me/delete/", delete_profile),
    path('', include(router.urls)),
]