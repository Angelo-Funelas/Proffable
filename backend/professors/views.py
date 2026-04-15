from django.shortcuts import render
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.conf import settings
import requests, threading

from .serializers import ProfessorSerializer, ProfessorOverviewSerializer, ReviewSerializer, InstitutionSerializer, InstitutionDomainSerializer, CourseSerializer, ReviewReportSerializer
from .serializers import TagSerializer, FavoriteProfSerializer
from .models import Professor, Review, Institution, InstitutionDomain, Course, ReviewReport, ReviewVote, Tag, FavoriteProf, ProfessorOverview
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import IntegrityError
from django.db.models import Avg, Count, Case, When, Value, BooleanField, F, CharField
from .permissions import IsOwner, IsModeratorOrReadOnly, IsModerator
from django.db.models.functions import Concat
from django.db.models import Count, Q
from django.db.models.functions import Lower
# Create your views here.

class ProfessorViewSet(viewsets.ModelViewSet):
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer
    permission_classes = [IsModeratorOrReadOnly]

    filter_backends = [filters.SearchFilter]
    search_fields = ['f_name', 'l_name']

    def get_queryset(self):
        queryset = Professor.objects.annotate(
            avg_rating=Avg("reviews__review_rating"),
            review_count=Count("reviews", distinct=True),
            full_name=Concat('f_name', Value(' '), 'l_name'),
            favorite_count=Count("fave_prof", distinct=True)
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

    @action(detail=True, methods=['get'])    
    def similar(self, request, pk=None):
        professor = self.get_object()

        tag_ids = Tag.objects.filter(
            review_tag__review_id__professor=professor
        ).values_list('tag_id', flat=True)
        
        similar = Professor.objects.filter(
            reviews__review_tag__tag_id__in=tag_ids
        ).exclude(pk=pk).annotate(
            avg_rating=Avg("reviews__review_rating"),
            review_count=Count("reviews", distinct=True),
            favorite_count=Count("fave_prof", distinct=True)
        ).distinct()[:5]
        
        return Response(ProfessorSerializer(similar, many=True, context={'request': request}).data)
      
    @action(detail=True, methods=['get'], permission_classes=[AllowAny])
    def analytics(self, request, pk=None):
        professor = self.get_object()

        valid_reviews = professor.reviews.exclude(
            Q(received_grade__isnull=True) | 
            Q(received_grade__exact="") | 
            Q(received_grade__regex=r'^\s*$')
        )

        total_with_grades = valid_reviews.count()

        if total_with_grades == 0:
            return Response({
                "distribution": [], 
                "total_reviews": 0
            })

        grade_counts = valid_reviews.annotate(
            normalized_grade=Lower('received_grade')
        ).values('normalized_grade').annotate(
            count=Count('normalized_grade')
        ).order_by('normalized_grade')

        distribution = [
            {
                "grade": item['normalized_grade'].upper(),
                "count": item['count'],
                "percentage": round((item['count'] / total_with_grades) * 100, 2)
            }
            for item in grade_counts
        ]

        return Response({
            "distribution": distribution,
            "total_reviews": total_with_grades
        })

class ProfessorOverviewViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ProfessorOverview.objects.all()
    serializer_class = ProfessorOverviewSerializer
    
    lookup_field = 'professor_id'

PROMPT_FILE_PATH = settings.BASE_DIR / 'professors' / 'prompts' / 'system_prompt.txt'
try:
    with open(PROMPT_FILE_PATH, 'r', encoding='utf-8') as file:
        SYSTEM_PROMPT = file.read().strip()
except FileNotFoundError:
    print(f"⚠️ Warning: Could not find prompt file at {PROMPT_FILE_PATH}")
    
def summarize_reviews(professor):
    if SYSTEM_PROMPT is None: return
    url = settings.LLM_API_URL
    headers = {
        "Content-Type": "application/json",
        "x-api-key": settings.LLM_API_KEY
    }
    payload = {
        "model": "gemma3:12b", 
        "messages": [],
    }
    sys_message = {
        "role": "system",
        "content": SYSTEM_PROMPT
    }
    payload['messages'].append(sys_message)
    reviews = Review.objects.filter(professor=professor)
    for review in reviews:
        message = {
            "role": "user",
            "content": f"Review by Student #{review.student.id}: {review.comment_text}"
        }
        if len(review.comment_text) > 0:
            payload['messages'].append(message)

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status() 
        result = response.json()
        
        print("🤖 Model Output:\n")
        output = result.get("response", "No response field found.")
        print(output)
        ProfessorOverview.objects.update_or_create(professor=professor, defaults={'overview': output})
        
    except requests.exceptions.HTTPError as errh:
        print(f"❌ HTTP Error: {errh}")
        # Print the specific error message sent by the Express server
        print(f"Server details: {response.json()}") 
    except requests.exceptions.RequestException as err:
        print(f"❌ Connection Error: {err}")
        
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Review.objects.select_related("professor", "student").all()
        professor_id = self.request.query_params.get('professor')
        mine = self.request.query_params.get('mine')

        if professor_id:
            queryset = queryset.filter(professor_id=professor_id)

        if mine in ["true", "1", "True"]:
            if user.is_authenticated:
                queryset = queryset.filter(student=user)
            else:
                return Review.objects.none()

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
            return [IsAuthenticated(), (IsOwner | IsModerator)()]
        return [AllowAny()]

    def perform_create(self, serializer):
        try:
            instance = serializer.save(student=self.request.user)
            thread = threading.Thread(
                target=summarize_reviews, 
                args=(instance.professor,)
            )
            thread.start()
        except IntegrityError:
            raise serializer.ValidationError("You have already reviewed this professor.")
    
    
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
    
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.is_moderator:
            return ReviewReport.objects.filter(reporter__institution=user.institution).annotate(
                author=Concat(
                    F('review__student__f_name'),
                    Value(' '),
                    F('review__student__l_name'),
                    Value(' ('),
                    F('review__student__email'),
                    Value(')'),
                    output_field=CharField()
                )
            )
        return ReviewReport.objects.none()

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]
        else:
            return [IsModerator()]

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
    
    @action(detail=True, methods=['post'])
    def dismiss(self, request, pk=None):
        report = self.get_object()
        report.delete()
        return Response({'status': 'report dismissed'})

class InstitutionViewSet(viewsets.ModelViewSet):
    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer
    permission_classes = [AllowAny]

class InstitutionDomainViewSet(viewsets.ModelViewSet):
    queryset = InstitutionDomain.objects.all()
    serializer_class = InstitutionDomainSerializer
    
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return InstitutionDomain.objects.filter(institution=user.institution)
        return InstitutionDomain.objects.none()
    
    def perform_create(self, serializer):
        serializer.save(institution=self.request.user.institution)
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsModerator()]
        return []

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

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return FavoriteProf.objects.filter(student=user).select_related("professor", "student")
        return FavoriteProf.objects.none()

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)
    
    def get_permissions(self):
        return [IsAuthenticated()]