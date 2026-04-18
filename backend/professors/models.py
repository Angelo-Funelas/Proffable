from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.functions import Lower
from api.models import User
from django.conf import settings

# Create your models here.
class Institution(models.Model):
    institution_id = models.AutoField(primary_key=True)
    name = models.CharField(blank=False, max_length=255)
    def __str__(self):
        return f"{self.name}"

class InstitutionDomain(models.Model):
    institution = models.ForeignKey(Institution, null=True, blank=True, on_delete=models.SET_NULL, related_name="domains")
    domain = models.CharField(blank=False, max_length=32, unique=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower('domain'),
                name='unique_domain'
            ),
        ]

class Course(models.Model):
    course_id = models.AutoField(primary_key=True)
    course_code = models.CharField(blank=False, max_length=50)
    course_name = models.CharField(blank=False, max_length=255)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name="courses")

    def __str__(self):
        return f"{self.course_code}"

class Professor(models.Model):
    professor_id = models.AutoField(primary_key=True)
    f_name = models.CharField(blank=False, max_length=32)
    l_name = models.CharField(blank=False, max_length=32)
    m_name = models.CharField(blank=True, max_length=32)
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return f"{self.l_name}, {self.f_name}"

class ProfessorOverview(models.Model):
    professor = models.OneToOneField(Professor, on_delete=models.CASCADE, related_name="overview")
    last_updated = models.DateTimeField(auto_now=True)
    overview = models.TextField()

class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name="reviews")
    review_rating = models.IntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment_text = models.TextField()
    review_date = models.DateField(auto_now_add=True)
    received_grade = models.CharField(max_length=10, blank=True)
    helpful_count = models.PositiveIntegerField(default=0)
    course = models.ForeignKey(Course,on_delete=models.CASCADE, related_name="review_course")
    
    SEMESTER_CHOICES = [
        ("1st", "1st Semester"),
        ("2nd", "2nd Semester"),
        ("summer", "Summer"),
    ]
    semester_term = models.CharField(choices=SEMESTER_CHOICES,null=False, blank=False)

    #of the format 20XX-20XX, validated in serializer
    semester_year = models.CharField(max_length=9, null=False, blank=False)
    
    def __str__(self):
        return f"{self.review_id}"
    
    class Meta:
        unique_together = ("student", "professor", "course", "semester_term", "semester_year")

        
class ReviewVote(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="votes")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("review", "user")

class ReviewReport(models.Model):
    REPORT_REASON_CHOICES = [
        ("offensive", "Offensive Language"),
        ("spam", "Spam or Advertising"),
        ("fake", "Fake Review"),
        ("harassment", "Harassment or Hate Speech"),
        ("irrelevant", "Irrelevant Content"),
        ("other", "Other"),
    ]

    report_id = models.AutoField(primary_key=True)
    review = models.ForeignKey("Review", on_delete=models.CASCADE, related_name="reports")
    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    reason = models.CharField(max_length=50, choices=REPORT_REASON_CHOICES)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class ProfessorCourse(models.Model):
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name="professor_course")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="professor_course")

    class Meta:
        unique_together = ("professor", "course")


class Tag(models.Model):
    tag_id = models.AutoField(primary_key=True)
    tag_name = models.CharField(blank=False, max_length=32)


class ReviewTag(models.Model):
    review_id = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="review_tag")
    tag_id = models.ForeignKey(Tag,on_delete=models.CASCADE, related_name="review_tag")

    class Meta:
        unique_together = ("review_id", "tag_id")


class FavoriteProf(models.Model):
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name="fave_prof")
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="fave_prof")

    class Meta:
        unique_together = ("professor","student")