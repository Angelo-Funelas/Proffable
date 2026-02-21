from rest_framework import serializers
from .models import Professor, Review

class ProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professor
        fields = ["professor_id","f_name","l_name","m_name","email"]

class ReviewSerializer(serializers.ModelSerializer):
    student_name = serializers.StringRelatedField(source="student", read_only=True)
    professor_name = serializers.StringRelatedField(source="professor", read_only=True)

    class Meta:
        model = Review
        fields = ["review_id", "student", "student_name", "professor", "professor_name",
            "review_rating", "comment_text", "review_date", "received_grade"]