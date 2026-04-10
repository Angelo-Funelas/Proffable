from rest_framework import serializers
from .models import Professor, Review, Institution, Course, ReviewReport, Tag, ReviewTag, FavoriteProf
from django.db.models import Count

class ProfessorSerializer(serializers.ModelSerializer):
    avg_rating = serializers.FloatField(read_only=True)    
    review_count = serializers.IntegerField(read_only=True)
    favorite_count = serializers.IntegerField(read_only=True)
    is_favorited = serializers.SerializerMethodField()
    favorite_id = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()

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

    def get_tags(self,obj):
        tags = Tag.objects.filter(review_tag__review_id__professor=obj)\
            .annotate(count=Count('review_tag'))\
            .order_by('-count')[:5]
        return [tag.tag_name for tag in tags]

    class Meta:
        model = Professor
        fields = ["professor_id", "f_name", "l_name", "m_name", "email", 
                  "avg_rating", "review_count", "favorite_count", "is_favorited", "favorite_id", "tags"]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields=["tag_id","tag_name"]


class ReviewTagSerializer(serializers.ModelSerializer):
    tag_name = serializers.ReadOnlyField(source="tag_id.tag_name")

    class Meta:
        model = ReviewTag
        fields = ["tag_name"]



class ReviewSerializer(serializers.ModelSerializer):
    professor_name = serializers.StringRelatedField(source="professor", read_only=True)
    helpful_count = serializers.IntegerField(read_only=True)
    is_owner = serializers.BooleanField(read_only=True)
    tags = serializers.PrimaryKeyRelatedField(
        source="review_tag",
        many=True,
        queryset=Tag.objects.all(),
        write_only=True
    )
    read_tags = ReviewTagSerializer(source="review_tag", many=True, read_only=True)

    class Meta:
        model = Review
        fields = [
            "review_id", "professor", "professor_name", "is_owner",
            "review_rating", "comment_text", "review_date", "received_grade", 
            "helpful_count", "tags", "read_tags"
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


class InstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = ['institution_id', 'name']


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['course_id', 'course_code']


class ReviewReportSerializer(serializers.ModelSerializer):
    reporter_name = serializers.StringRelatedField(source="reporter", read_only=True)

    class Meta:
        model = ReviewReport
        fields = [
            "report_id",
            "review",
            "reason",
            "description",
            "created_at",
            "reporter_name"
        ]
        read_only_fields = ["report_id", "created_at"]

class FavoriteProfSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    professor_name = serializers.StringRelatedField(source="professor", read_only=True)
    student_name = serializers.StringRelatedField(source="student", read_only=True)
    professor_id = serializers.PrimaryKeyRelatedField(source="professor", queryset=Professor.objects.all(), write_only=True)
    f_name = serializers.ReadOnlyField(source="professor.f_name")
    m_name = serializers.ReadOnlyField(source="professor.m_name")
    l_name = serializers.ReadOnlyField(source="professor.l_name")
    email = serializers.ReadOnlyField(source="professor.email")

    class Meta:
        model = FavoriteProf
        fields = [
            'id',
            'professor_id',
            'professor_name',
            'student_name',
            'f_name',
            'm_name',
            'l_name',
            'email',
        ]
