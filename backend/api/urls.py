from django.urls import path, include
from rest_framework.routers import DefaultRouter

from professors.views import ProfessorViewSet

router = DefaultRouter()
router.register(r"professors",ProfessorViewSet)

urlpatterns = [
    path('', include(router.urls)),
]