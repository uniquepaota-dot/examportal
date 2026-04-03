from django.contrib import admin
from django.urls import path, include
from accounts import views as account_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', account_views.dashboard_redirect, name='index'),
    path('', include('accounts.urls')),
    path('exams/', include('exams.urls', namespace='exams')),
    path('results/', include('results.urls', namespace='results')),
]
