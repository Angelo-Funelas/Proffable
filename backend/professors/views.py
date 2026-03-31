from django.shortcuts import render
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated, AllowAny

from .serializers import ProfessorSerializer, ReviewSerializer, InstitutionSerializer, CourseSerializer, ReviewReportSerializer
from .serializers import TagSerializer, FavoriteProfSerializer
from .models import Professor, Review, Institution, Course, ReviewReport, ReviewVote, Tag, FavoriteProf
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import IntegrityError
from django.db.models import Avg, Count, Case, When, Value, BooleanField
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

    def get_queryset(self):
        user = self.request.user
        queryset = Review.objects.all()
        professor_id = self.request.query_params.get('professor')
        if professor_id:
            queryset = queryset.filter(professor_id=professor_id)
        if user.is_authenticated:
            queryset = queryset.annotate(
                is_owner=Case(
                    When(student=user, then=Value(True)),
                    default=Value(False),
                    output_field=BooleanField(),
                )
            )
        else:
            queryset = queryset.annotate(
                is_owner=Value(False, output_field=BooleanField())
            )
        return queryset

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]
        # Only owners can update, partially update, or delete their reviews.
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsOwner()]
        return [AllowAny()]

    def perform_create(self, serializer):
        try:
            serializer.save(student=self.request.user)
        except IntegrityError:
            raise serializers.ValidationError("You have already reviewed this professor.")
    
    
    @action(detail=True, methods=["post"])
    def vote(self, request, pk=None):
        review = self.get_object()
        user = request.user if request.user.is_authenticated else None

        existing_vote = ReviewVote.objects.filter(review=review, user=user).first()

        if existing_vote:
            existing_vote.delete()
            review.helpful_count = max(0, review.helpful_count - 1)
            review.save()
            return Response({"helpful_count": review.helpful_count, "voted": False})
        else:
            ReviewVote.objects.create(review=review, user=user)
            review.helpful_count += 1
            review.save()
            return Response({"helpful_count": review.helpful_count, "voted": True})
   
    @action(detail=True, methods=["get"])
    def has_voted(self, request, pk=None):
        review = self.get_object()
        user = request.user if request.user.is_authenticated else None
        voted = ReviewVote.objects.filter(review=review, user=user).exists()
        return Response({"voted": voted})


class ReviewReportViewSet(viewsets.ModelViewSet):
    queryset = ReviewReport.objects.all()
    serializer_class = ReviewReportSerializer

    def perform_create(self, serializer):
        reporter = self.request.user if self.request.user.is_authenticated else None
        serializer.save(reporter=reporter)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def helpful(self, request, pk=None):
        review = self.get_object()
        user = request.user

        vote, created = ReviewVote.objects.get_or_create(
            user=user,
            review=review,
            defaults={'is_helpful': True}
        )
        if not created:
            vote.is_helpful = not vote.is_helpful
            vote.save()

        return Response({'helpful_count': review.votes.filter(is_helpful=True).count()})

class InstitutionViewSet(viewsets.ModelViewSet):
    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer
    permission_classes = [AllowAny]

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [AllowAny]


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny]


class FavoriteProfViewset(viewsets.ModelViewSet):
    queryset = FavoriteProf.objects.all()
    serializer_class = FavoriteProfSerializer

    def perform_create(self, serializer):
        student = self.request.user if self.request.user.is_authenticated else None
        serializer.save(student=student)
    
    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            return [IsAuthenticated()]
        return []