from django.urls import path, include
from rest_framework.routers import DefaultRouter

from professors.views import ProfessorViewSet, ReviewViewSet

router = DefaultRouter()
router.register(r"professors",ProfessorViewSet)
router.register(r"reviews",ReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),
]