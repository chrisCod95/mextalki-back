from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from src.api.views import ScheduledEventListView, ScheduledEventView, TeacherListView

urlpatterns = [
    path('scheduled_events/', ScheduledEventListView.as_view()),
    path('scheduled_events/<uuid:pk>', ScheduledEventView.as_view()),
    path('teachers/', TeacherListView.as_view()),
]

urlpatterns = format_suffix_patterns(
    urlpatterns,
    allowed=['json'],
)
