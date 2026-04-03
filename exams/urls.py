from django.urls import path
from . import views

app_name = 'exams'

urlpatterns = [
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/exam/create/', views.exam_create_view, name='exam_create'),
    path('admin/exam/<int:pk>/edit/', views.exam_edit_view, name='exam_edit'),
    path('admin/exam/<int:pk>/questions/add/', views.add_question_view, name='add_question'),
    path('admin/exam/<int:pk>/import/', views.import_questions_view, name='import_questions'),
    path('admin/exam/<int:pk>/delete/', views.exam_delete_view, name='delete_exam'),
    path('admin/students/', views.student_list_view, name='student_list'),
    path('admin/students/<int:pk>/toggle/', views.toggle_student_status_view, name='toggle_student_status'),
    path('admin/students/<int:pk>/delete/', views.delete_student_view, name='delete_student'),
    path('admin/students/<int:pk>/reset-password/', views.reset_student_password_view, name='reset_student_password'),
    path('admin/students/<int:pk>/assign-exams/', views.assign_exams_view, name='assign_exams'),
    path('admin/all-results/', views.all_results_view, name='all_results'),
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    path('exam/<int:pk>/', views.exam_detail_view, name='exam_detail'),
    path('exam/<int:pk>/take/', views.take_exam_view, name='take_exam'),
]
