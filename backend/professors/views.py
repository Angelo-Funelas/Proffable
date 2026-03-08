from django.shortcuts import render
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import ProfessorSerializer, ReviewSerializer
from .models import Professor, Review
from .permissions import IsOwner
from django.db.models import Avg, Count
# Create your views here.

class ProfessorViewSet(viewsets.ModelViewSet):
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer

    filter_backends = [filters.SearchFilter]
    search_fields = ['f_name', 'l_name']

    def get_queryset(self):

        qs = Professor.objects.annotate(
            avg_rating = Avg("reviews__review_rating"),
            review_count = Count("reviews")
        )

        min_rating = self.request.query_params.get("min_rating")
        if min_rating:
            qs = qs.filter(avg_rating__gte=min_rating)
        return qs
        

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