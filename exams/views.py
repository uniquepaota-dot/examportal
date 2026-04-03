from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Exam, Question
from .forms import ExamForm, QuestionForm
from django.contrib import messages
import csv
import openpyxl
from io import TextIOWrapper
from django.contrib.auth import get_user_model
from results.models import Result
import random
import string
User = get_user_model()

def is_admin(user):
    return user.is_authenticated and (user.is_admin or user.is_superuser)

def is_student(user):
    return user.is_authenticated and user.is_student

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    exams = Exam.objects.all().order_by('-date')
    return render(request, 'exams/admin_dashboard.html', {'exams': exams})

@login_required
@user_passes_test(is_admin)
def exam_create_view(request):
    if request.method == 'POST':
        form = ExamForm(request.POST)
        if form.is_valid():
            exam = form.save()
            messages.success(request, f'Exam "{exam.title}" created successfully!')
            return redirect('exams:admin_dashboard')
    else:
        form = ExamForm()
    return render(request, 'exams/exam_form.html', {'form': form, 'title': 'Create Exam'})

@login_required
@user_passes_test(is_admin)
def exam_edit_view(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    if request.method == 'POST':
        form = ExamForm(request.POST, instance=exam)
        if form.is_valid():
            form.save()
            messages.success(request, f'Exam "{exam.title}" updated successfully!')
            return redirect('exams:admin_dashboard')
    else:
        form = ExamForm(instance=exam)
    return render(request, 'exams/exam_form.html', {'form': form, 'title': 'Edit Exam'})

@login_required
@user_passes_test(is_admin)
def add_question_view(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.exam = exam
            question.save()
            messages.success(request, 'Question added successfully!')
            if 'add_another' in request.POST:
                return redirect('exams:add_question', pk=pk)
            return redirect('exams:admin_dashboard')
    else:
        form = QuestionForm()
    return render(request, 'exams/question_form.html', {'form': form, 'exam': exam})

@login_required
@user_passes_test(is_student)
def student_dashboard(request):
    # Only show exams assigned to this student
    exams = request.user.assigned_exams.filter(is_published=True).order_by('-date')
    results = request.user.results.all().order_by('-submitted_at')
    return render(request, 'exams/student_dashboard.html', {
        'exams': exams,
        'results': results
    })

@login_required
@user_passes_test(is_student)
def exam_detail_view(request, pk):
    # Ensure the exam is assigned to the student
    exam = get_object_or_404(request.user.assigned_exams, pk=pk, is_published=True)
    return render(request, 'exams/exam_detail.html', {'exam': exam})

@login_required
@user_passes_test(is_student)
def take_exam_view(request, pk):
    # Ensure the exam is assigned to the student
    exam = get_object_or_404(request.user.assigned_exams, pk=pk, is_published=True)
    questions = exam.questions.all()
    
    if not questions.exists():
        messages.error(request, 'This exam has no questions yet.')
        return redirect('exams:student_dashboard')
        
    return render(request, 'exams/take_exam.html', {
        'exam': exam,
        'questions': questions
    })

@login_required
@user_passes_test(is_admin)
def import_questions_view(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        file_name = file.name
        
        try:
            if file_name.endswith('.xlsx'):
                wb = openpyxl.load_workbook(file)
                sheet = wb.active
                for row in sheet.iter_rows(min_row=2, values_only=True):
                    if not row or not any(row): continue
                    
                    try:
                        q_text = str(row[0]).strip() if row[0] is not None else ""
                        if not q_text: continue
                        
                        opt1 = str(row[1]).strip() if row[1] is not None else ""
                        opt2 = str(row[2]).strip() if row[2] is not None else ""
                        opt3 = str(row[3]).strip() if row[3] is not None else ""
                        opt4 = str(row[4]).strip() if row[4] is not None else ""
                        ans_text = str(row[5]).strip().lower() if len(row) > 5 and row[5] is not None else ""
                        
                        # Logic to determine option number from text
                        correct_num = None
                        if ans_text in ['1', '2', '3', '4']:
                            correct_num = int(ans_text)
                        elif ans_text == opt1.lower(): correct_num = 1
                        elif ans_text == opt2.lower(): correct_num = 2
                        elif ans_text == opt3.lower(): correct_num = 3
                        elif ans_text == opt4.lower(): correct_num = 4
                        
                        if correct_num:
                            Question.objects.create(
                                exam=exam,
                                question_text=q_text,
                                option1=opt1, option2=opt2, option3=opt3, option4=opt4,
                                correct_answer=correct_num
                            )
                    except Exception:
                        continue
            elif file_name.endswith('.csv'):
                csv_file = TextIOWrapper(file.file, encoding='utf-8')
                reader = csv.reader(csv_file)
                next(reader, None)
                for row in reader:
                    if not row or not any(row): continue
                    
                    try:
                        q_text = row[0].strip() if len(row) > 0 else ""
                        if not q_text: continue
                        
                        opt1 = row[1].strip() if len(row) > 1 else ""
                        opt2 = row[2].strip() if len(row) > 2 else ""
                        opt3 = row[3].strip() if len(row) > 3 else ""
                        opt4 = row[4].strip() if len(row) > 4 else ""
                        ans_text = row[5].strip().lower() if len(row) > 5 else ""
                        
                        correct_num = None
                        if ans_text in ['1', '2', '3', '4']:
                            correct_num = int(ans_text)
                        elif ans_text == opt1.lower(): correct_num = 1
                        elif ans_text == opt2.lower(): correct_num = 2
                        elif ans_text == opt3.lower(): correct_num = 3
                        elif ans_text == opt4.lower(): correct_num = 4
                        
                        if correct_num:
                            Question.objects.create(
                                exam=exam,
                                question_text=q_text,
                                option1=opt1, option2=opt2, option3=opt3, option4=opt4,
                                correct_answer=correct_num
                            )
                    except Exception:
                        continue
            
            messages.success(request, 'Questions imported successfully!')
            return redirect('exams:admin_dashboard')
        except Exception as e:
            messages.error(request, f'Error importing questions: {str(e)}')
            
    return render(request, 'exams/import_questions.html', {'exam': exam})

@login_required
@user_passes_test(is_admin)
def exam_delete_view(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    return redirect('exams:admin_dashboard')

@login_required
@user_passes_test(is_admin)
def student_list_view(request):
    students = User.objects.filter(is_student=True).order_by('-date_joined')
    return render(request, 'exams/student_list.html', {'students': students})

@login_required
@user_passes_test(is_admin)
def all_results_view(request):
    results = Result.objects.all().order_by('-submitted_at')
    return render(request, 'results/all_results.html', {'results': results})

@login_required
@user_passes_test(is_admin)
def toggle_student_status_view(request, pk):
    student = get_object_or_404(User, pk=pk, is_student=True)
    student.is_active = not student.is_active
    student.save()
    messages.success(request, f'Status of {student.username} updated.')
    return redirect('exams:student_list')

@login_required
@user_passes_test(is_admin)
def delete_student_view(request, pk):
    student = get_object_or_404(User, pk=pk, is_student=True)
    username = student.username
    student.delete()
    messages.success(request, f'Student {username} deleted.')
    return redirect('exams:student_list')

@login_required
@user_passes_test(is_admin)
def reset_student_password_view(request, pk):
    student = get_object_or_404(User, pk=pk, is_student=True)
    # Generate random password
    new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    student.set_password(new_password)
    student.save()
    messages.success(request, f'Password for {student.username} reset to: {new_password}')
    return redirect('exams:student_list')

@login_required
@user_passes_test(is_admin)
def assign_exams_view(request, pk):
    student = get_object_or_404(User, pk=pk, is_student=True)
    if request.method == 'POST':
        exam_ids = request.POST.getlist('exams')
        student.assigned_exams.clear()
        if exam_ids:
            exams = Exam.objects.filter(id__in=exam_ids)
            for exam in exams:
                exam.assigned_students.add(student)
        messages.success(request, f'Exams assigned to {student.username}.')
        return redirect('exams:student_list')
    
    exams = Exam.objects.filter(is_published=True)
    assigned_exam_ids = student.assigned_exams.values_list('id', flat=True)
    return render(request, 'exams/assign_exams.html', {
        'student': student,
        'exams': exams,
        'assigned_exam_ids': assigned_exam_ids
    })
