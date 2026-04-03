from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from exams.models import Exam, Question
from .models import Result, StudentAnswer
from django.contrib import messages

@login_required
def submit_exam_view(request, pk):
    if request.method == 'POST':
        exam = get_object_or_404(Exam, pk=pk)
        questions = exam.questions.all()
        score = 0
        total_questions = questions.count()
        
        # We'll calculate marks proportionately. If default is 100 total, 
        # each question is worth total_marks / num_questions.
        marks_per_question = exam.total_marks / total_questions if total_questions > 0 else 0
        
        for question in questions:
            selected_option = request.POST.get(f'question_{question.id}')
            if selected_option:
                selected_option = int(selected_option)
                # Save student's answer
                StudentAnswer.objects.create(
                    student=request.user,
                    question=question,
                    selected_answer=selected_option
                )
                # Check if correct
                if selected_option == question.correct_answer:
                    score += marks_per_question
        
        # Save Result
        result = Result.objects.create(
            student=request.user,
            exam=exam,
            score=int(score)
        )
        
        messages.success(request, f'Exam "{exam.title}" submitted successfully!')
        return redirect('results:result_detail', pk=result.pk)
    
    return redirect('exams:student_dashboard')

@login_required
def result_detail_view(request, pk):
    # Admins can see all results; students can only see their own
    if request.user.is_admin or request.user.is_superuser:
        result = get_object_or_404(Result, pk=pk)
    else:
        result = get_object_or_404(Result, pk=pk, student=request.user)
    return render(request, 'results/result_detail.html', {'result': result})
