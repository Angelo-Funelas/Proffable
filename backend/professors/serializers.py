from rest_framework import serializers
from .models import Professor, Review, Institution, Course, ReviewReport

class ProfessorSerializer(serializers.ModelSerializer):
    avg_rating = serializers.FloatField(read_only=True)    
    review_count = serializers.IntegerField(read_only=True)
    # Add this line to pull the name from the related Institution model
    institution_name = serializers.CharField(source='institution.name', read_only=True)

    class Meta:
        model = Professor
        fields = [
            "professor_id", "f_name", "l_name", "m_name", "email", 
            "institution_name", "avg_rating", "review_count"
        ]

class ReviewSerializer(serializers.ModelSerializer):
    student_name = serializers.StringRelatedField(source="student", read_only=True)
    professor_name = serializers.StringRelatedField(source="professor", read_only=True)

    class Meta:
        model = Review
        fields = ["review_id", "student", "student_name", "professor", "professor_name",
            "review_rating", "comment_text", "review_date", "received_grade", "helpful_count"]
        extra_kwargs = {
            'student': {'read_only': True}
        }

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