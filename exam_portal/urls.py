from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/dashboard/', permanent=True)),
    path('', include('accounts.urls')),
    path('exams/', include('exams.urls', namespace='exams')),
    path('results/', include('results.urls', namespace='results')),
]
