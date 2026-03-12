from django.contrib import admin
from .models import Professor, Review, Institution, Course, ProfessorCourse, ReviewVote

class ProfessorAdmin(admin.ModelAdmin):
    model = Professor

class ReviewAdmin(admin.ModelAdmin):
    model = Review

class InstitutionAdmin(admin.ModelAdmin):
    model = Institution

class CourseAdmin(admin.ModelAdmin):
    model = Course

class ProfessorCourseAdmin(admin.ModelAdmin):
    model = ProfessorCourse

admin.site.register(Professor, ProfessorAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Institution, InstitutionAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(ProfessorCourse, ProfessorCourseAdmin)
admin.site.register(ReviewVote)