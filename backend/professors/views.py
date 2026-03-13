from django.shortcuts import render
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import ProfessorSerializer, ReviewSerializer, InstitutionSerializer, CourseSerializer
from .models import Professor, Review, Institution, Course
from django.db.models import Avg, Count, Value
from .permissions import IsOwner
from django.db.models.functions import Concat
# Create your views here.

class ProfessorViewSet(viewsets.ModelViewSet):
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer

    filter_backends = [filters.SearchFilter]
    search_fields = ['f_name', 'l_name']

    def get_queryset(self):
        queryset = Professor.objects.annotate(
            avg_rating=Avg("reviews__review_rating"),
            review_count=Count("reviews"),
            full_name = Concat('f_name', Value(' '), 'l_name')
        )
        search = self.request.query_params.get('search')
        inst_name = self.request.query_params.get('institution')
        course_code = self.request.query_params.get('course')
    
        if search and search != 'undefined':
            queryset = queryset.filter(full_name__icontains=search)
        
        if inst_name and inst_name != 'undefined':
            queryset = queryset.filter(professor_course__course__institution__name__iexact=inst_name)
            
        if course_code and course_code != 'undefined':
            queryset = queryset.filter(professor_course__course__course_code__iexact=course_code)

        min_rating = self.request.query_params.get("min_rating")
        if min_rating:
            queryset = queryset.filter(avg_rating__gte=min_rating)

        print("Final Query: ", str(queryset.query))
        return queryset
        
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]
        # Only owners can update, partially update, or delete their reviews.
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsOwner()]
        return [AllowAny()]

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)

class InstitutionViewSet(viewsets.ModelViewSet):
    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer
    permission_classes = [AllowAny]

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [AllowAny]