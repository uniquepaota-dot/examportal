from django.contrib import admin
from .models import Exam, Question

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1

class ExamAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]
    list_display = ('title', 'total_marks', 'duration', 'is_published', 'date')

admin.site.register(Exam, ExamAdmin)
admin.site.register(Question)
