from django.shortcuts import render
from rest_framework import viewsets
from .serializers import ProfessorSerializer
from .models import Professor
# Create your views here.

class ProfessorViewSet(viewsets.ModelViewSet):
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer

