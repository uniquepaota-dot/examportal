from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('exams/', include('exams.urls', namespace='exams')),
    path('results/', include('results.urls', namespace='results')),
]
