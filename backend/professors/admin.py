from django.contrib import admin
from .models import Professor, Review
# Register your models here.

class ProfessorAdmin(admin.ModelAdmin):
    model = Professor

class ReviewAdmin(admin.ModelAdmin):
    model = Review

admin.site.register(Professor, ProfessorAdmin)
admin.site.register(Review, ReviewAdmin)