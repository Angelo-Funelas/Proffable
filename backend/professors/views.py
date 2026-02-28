from django.shortcuts import render
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import ProfessorSerializer, ReviewSerializer
from .models import Professor, Review
from .permissions import IsOwner
# Create your views here.

class ProfessorViewSet(viewsets.ModelViewSet):
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer

    filter_backends = [filters.SearchFilter]
    search_fields = ['f_name', 'l_name']

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_permissions(self):
        # If submitting a new review, require authentication.
        if self.action == 'create':
            return [IsAuthenticated()]
        # Only owners can update, partially update, or delete their reviews.
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsOwner()]
        return [AllowAny()]

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)