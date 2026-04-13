from django.contrib import admin
from .models import Professor, ProfessorOverview, Review, Institution, InstitutionDomain, Course, ProfessorCourse, ReviewReport, ReviewVote, Tag, ReviewTag
from .models import FavoriteProf

class ProfessorAdmin(admin.ModelAdmin):
    model = Professor

class ProfessorOverviewAdmin(admin.ModelAdmin):
    model = ProfessorOverview

class InstitutionAdmin(admin.ModelAdmin):
    model = Institution
    
class InstitutionDomainAdmin(admin.ModelAdmin):
    model = InstitutionDomain

class CourseAdmin(admin.ModelAdmin):
    model = Course

class ProfessorCourseAdmin(admin.ModelAdmin):
    model = ProfessorCourse

class TagAdmin(admin.ModelAdmin):
    model = Tag

class ReviewTagInline(admin.StackedInline):
    model = ReviewTag

class ReviewReportAdmin(admin.ModelAdmin): 
    model = ReviewReport

class ReviewAdmin(admin.ModelAdmin):
    model = Review
    inlines = [ReviewTagInline]

class FavoriteAdmin(admin.ModelAdmin):
    model = FavoriteProf


admin.site.register(Professor, ProfessorAdmin)
admin.site.register(ProfessorOverview, ProfessorOverviewAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Institution, InstitutionAdmin)
admin.site.register(InstitutionDomain, InstitutionDomainAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(ProfessorCourse, ProfessorCourseAdmin)
admin.site.register(ReviewVote)
admin.site.register(ReviewReport, ReviewReportAdmin)
admin.site.register(Tag,TagAdmin)
admin.site.register(ReviewTag)
admin.site.register(FavoriteProf, FavoriteAdmin)