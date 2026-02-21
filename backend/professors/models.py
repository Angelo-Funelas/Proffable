from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from api.models import User

# Create your models here.
class Professor(models.Model):
    professor_id = models.AutoField(primary_key=True)
    f_name = models.CharField(blank=False, max_length=32)
    l_name = models.CharField(blank=False, max_length=32)
    m_name = models.CharField(blank=True, max_length=32)
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return f"{self.l_name}, {self.f_name}"
    
class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name="reviews")
    review_rating = models.IntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment_text = models.TextField()
    review_date = models.DateField(auto_now_add=True)
    received_grade = models.CharField(max_length=10, blank=True)
    
    def __str__(self):
        return f"{self.review_id}"
    
    class Meta:
        unique_together = ("student", "professor")