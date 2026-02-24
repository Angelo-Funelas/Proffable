from django.urls import path, include
from rest_framework.routers import DefaultRouter

from professors.views import ProfessorViewSet, ReviewViewSet
from .views import login_view, logout_view, get_csrf_token

router = DefaultRouter()
router.register(r"professors",ProfessorViewSet)
router.register(r"reviews",ReviewViewSet)

urlpatterns = [
    path('csrf/', get_csrf_token, name='csrf'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('', include(router.urls)),
]