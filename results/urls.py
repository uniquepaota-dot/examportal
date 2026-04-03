from django.urls import path
from . import views

app_name = 'results'

urlpatterns = [
    path('submit/<int:pk>/', views.submit_exam_view, name='submit_exam'),
    path('result/<int:pk>/', views.result_detail_view, name='result_detail'),
]
