from django.contrib import admin
from .models import Professor, Review, Institution, Course, ProfessorCourse, ReviewReport, ReviewVote, Tag, ReviewTag
from .models import FavoriteProf

class ProfessorAdmin(admin.ModelAdmin):
    model = Professor



class InstitutionAdmin(admin.ModelAdmin):
    model = Institution

class CourseAdmin(admin.ModelAdmin):
    model = Course

class ProfessorCourseAdmin(admin.ModelAdmin):
    model = ProfessorCourse

class TagAdmin(admin.ModelAdmin):
    model = Tag

class ReviewTagInline(admin.StackedInline):
    model = ReviewTag

class ReviewReport(admin.ModelAdmin): 
    model = ReviewReport

class ReviewAdmin(admin.ModelAdmin):
    model = Review
    inlines = [ReviewTagInline]

class FavoriteAdmin(admin.ModelAdmin):
    model = FavoriteProf


admin.site.register(Professor, ProfessorAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Institution, InstitutionAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(ProfessorCourse, ProfessorCourseAdmin)
admin.site.register(ReviewVote)
admin.site.register(Tag,TagAdmin)
admin.site.register(ReviewTag)
admin.site.register(FavoriteProf, FavoriteAdmin)