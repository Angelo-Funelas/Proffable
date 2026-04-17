from rest_framework import serializers
from .models import Professor, ProfessorOverview, Review, Institution, InstitutionDomain,\
ProfessorCourse, Course, ReviewReport, Tag, ReviewTag, FavoriteProf
from django.db.models import Count
import re


class ProfessorSerializer(serializers.ModelSerializer):
    avg_rating = serializers.FloatField(read_only=True)    
    review_count = serializers.IntegerField(read_only=True)
    favorite_count = serializers.IntegerField(read_only=True)
    is_favorited = serializers.SerializerMethodField()
    favorite_id = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    institutions = serializers.SerializerMethodField()

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return FavoriteProf.objects.filter(professor=obj, student=request.user).exists()
        return False

    def get_favorite_id(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            fav = FavoriteProf.objects.filter(professor=obj, student=request.user).first()
            return fav.id if fav else None
        return None

    def get_tags(self, obj):
        tags = Tag.objects.filter(
            review_tag__review_id__professor=obj
        ).annotate(count=Count('review_tag')).order_by('-count')[:5]

        return TagSerializer(tags, many=True).data

    def get_institutions(self, obj):
        institutions = Institution.objects.filter(courses__professor_course__professor=obj).distinct()
        return InstitutionSerializer(institutions, many=True).data
    
    class Meta:
        model = Professor
        fields = ["professor_id", "f_name", "l_name", "m_name", "email", 
                  "avg_rating", "review_count", "favorite_count", "is_favorited", 
                  "favorite_id", "tags", "institutions"]


class ProfessorOverviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfessorOverview
        fields = ['id', 'professor', 'last_updated', 'overview']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["tag_id", "tag_name"]


class ReviewTagSerializer(serializers.ModelSerializer):
    tag_name = serializers.ReadOnlyField(source="tag_id.tag_name")

    class Meta:
        model = ReviewTag
        fields = ["tag_id","tag_name"]


class ReviewSerializer(serializers.ModelSerializer):
    professor_name = serializers.StringRelatedField(source="professor", read_only=True)
    professor_id = serializers.IntegerField(source="professor.professor_id", read_only=True)
    professor_f_name = serializers.CharField(source="professor.f_name", read_only=True)
    professor_m_name = serializers.CharField(source="professor.m_name", read_only=True)
    professor_l_name = serializers.CharField(source="professor.l_name", read_only=True)
    helpful_count = serializers.IntegerField(read_only=True)
    is_owner = serializers.BooleanField(read_only=True)
    tags = serializers.PrimaryKeyRelatedField(
        source="review_tag",
        many=True,
        queryset=Tag.objects.all(),
        write_only=True
    )
    read_tags = ReviewTagSerializer(source="review_tag", many=True, read_only=True)

    course = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all(),
    )
    course_code = serializers.CharField(source="course.course_code", read_only=True)
    course_name = serializers.CharField(source="course.course_name", read_only=True)
    semester_term = serializers.ChoiceField(choices=Review.SEMESTER_CHOICES)
    semester_year = serializers.CharField(max_length=9)
    read_semester_term = serializers.SerializerMethodField()

    def get_read_semester_term(self, obj):
        return obj.get_semester_term_display()

    class Meta:
        model = Review
        fields = [
            "review_id", "professor", "professor_id", "professor_name",
            "professor_f_name", "professor_m_name", "professor_l_name", "is_owner",
            "review_rating", "comment_text", "review_date", "received_grade", 
            "helpful_count", "tags", "read_tags", "course", "course_code", "course_name",
            "semester_term", "semester_year", "read_semester_term"
        ]
        extra_kwargs = {
            'student': {'read_only': True}
        }

    def create(self, validated_data):
        tags = validated_data.pop('review_tag', [])
        review = super().create(validated_data)
        for tag in tags:
            ReviewTag.objects.create(review_id=review, tag_id=tag)
        return review

    def update(self, instance, validated_data):
        tags = validated_data.pop('review_tag', None)
        review = super().update(instance, validated_data)
        if tags is not None:
            instance.review_tag.all().delete()
            for tag in tags:
                ReviewTag.objects.create(review_id=instance, tag_id=tag)
        return review

    def validate_semester_year(self, value):
        if not re.match(r"^\d{4}-\d{4}$", value):
            raise serializers.ValidationError("Format must be YYYY-YYYY e.g. 2024-2025.")
        start, end = value.split("-")
        if int(end) - int(start) != 1:
            raise serializers.ValidationError("Year range must be consecutive e.g. 2024-2025.")
        return value

    def validate(self, data):
        student = self.context["request"].user
        professor = data.get("professor")
        course = data.get("course")
        semester_term = data.get("semester_term")
        semester_year = data.get("semester_year")

        if course and not ProfessorCourse.objects.filter(
            professor=professor, course=course
        ).exists():
            raise serializers.ValidationError(
                {"course": "This professor does not teach that course."}
            )

        qs = Review.objects.filter(
            student=student,
            professor=professor,
            course=course,
            semester_term=semester_term,
            semester_year=semester_year,
        )

        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise serializers.ValidationError(
                "You have already reviewed this professor for this course and semester."
            )

        return data


class InstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = ['institution_id', 'name']

class InstitutionDomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstitutionDomain
        fields = ['domain', 'id']
        read_only_fields = ['institution']

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['course_id', 'course_code', 'course_name']


class ReviewReportSerializer(serializers.ModelSerializer):
    reporter_name = serializers.StringRelatedField(source="reporter", read_only=True)
    author = serializers.ReadOnlyField()
    class Meta:
        model = ReviewReport
        fields = [
            "report_id",
            "review",
            "reason",
            "description",
            "created_at",
            "reporter_name",
            "author"
        ]
        read_only_fields = ["report_id", "created_at"]

class FavoriteProfSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    professor_name = serializers.StringRelatedField(source="professor", read_only=True)
    student_name = serializers.StringRelatedField(source="student", read_only=True)

    # FIX: remove write_only=True so professor_id is included in GET responses too
    professor_id = serializers.PrimaryKeyRelatedField(
        source="professor",
        queryset=Professor.objects.all()
    )

    f_name = serializers.ReadOnlyField(source="professor.f_name")
    m_name = serializers.ReadOnlyField(source="professor.m_name")
    l_name = serializers.ReadOnlyField(source="professor.l_name")
    email = serializers.ReadOnlyField(source="professor.email")

    class Meta:
        model = FavoriteProf
        fields = [
            "id",
            "professor_id",
            "professor_name",
            "student_name",
            "f_name",
            "m_name",
            "l_name",
            "email",
        ]