from django.urls import path, include
from rest_framework.routers import DefaultRouter

from professors.views import ProfessorViewSet, ProfessorOverviewViewSet, ReviewViewSet, InstitutionViewSet, InstitutionDomainViewSet, CourseViewSet, ReviewReportViewSet
from professors.views import TagViewSet, FavoriteProfViewset
router = DefaultRouter()
router.register(r"professors",ProfessorViewSet)
router.register(r'overviews', ProfessorOverviewViewSet)
router.register(r"reviews",ReviewViewSet)
router.register(r"review-reports", ReviewReportViewSet)
router.register(r"institutions", InstitutionViewSet)
router.register(r"institution-domains", InstitutionDomainViewSet)
router.register(r"courses", CourseViewSet)
router.register(r"tags",TagViewSet)
router.register(r"favorite-prof", FavoriteProfViewset)


#include logic for jwt 
from .serializers import CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from .views import me, register_user, google_login, LoginView, update_profile, delete_profile
from professors.views import create_professor

urlpatterns = [
    path("token/", LoginView.as_view()),
    path("token/refresh/", TokenRefreshView.as_view()),
    path("register/", register_user),
    path("google-login/", google_login),
    path("me/", me),
    path("me/update/", update_profile),
    path("me/delete/", delete_profile),
    path("create-professor/", create_professor),
    path('', include(router.urls)),
]