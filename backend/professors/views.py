from django.shortcuts import render
from rest_framework import viewsets
from .serializers import ProfessorSerializer, ReviewSerializer
from .models import Professor, Review
# Create your views here.

class ProfessorViewSet(viewsets.ModelViewSet):
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer