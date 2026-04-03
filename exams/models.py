from django.db import models
from django.conf import settings

class Exam(models.Model):
    title = models.CharField(max_length=200)
    assigned_students = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='assigned_exams', blank=True)
    date = models.DateTimeField(auto_now_add=True)
    duration = models.IntegerField(help_text="Duration in minutes")
    total_marks = models.IntegerField(default=100)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Question(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    option1 = models.CharField(max_length=200)
    option2 = models.CharField(max_length=200)
    option3 = models.CharField(max_length=200)
    option4 = models.CharField(max_length=200)
    
    CORRECT_OPTIONS = (
        (1, 'Option 1'),
        (2, 'Option 2'),
        (3, 'Option 3'),
        (4, 'Option 4'),
    )
    correct_answer = models.IntegerField(choices=CORRECT_OPTIONS)

    def __str__(self):
        return self.question_text[:50]
