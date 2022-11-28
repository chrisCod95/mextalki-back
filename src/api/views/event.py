from django_filters.rest_framework import filters
from django_filters.rest_framework.filterset import FilterSet
from rest_framework.generics import ListAPIView, RetrieveAPIView

from src.api.serializers import ScheduledEventSerializer
from src.mextalki.models import ScheduledEvent


class ScheduledEventFilter(FilterSet):
    start_time = filters.DateTimeFilter(field_name='start_time', lookup_expr='gte')
    end_time = filters.DateTimeFilter(field_name='end_time', lookup_expr='lte')

    class Meta:
        model = ScheduledEvent
        fields = [
            'teacher',
        ]


class ScheduledEventListView(ListAPIView):
    queryset = ScheduledEvent.objects.order_by('start_time').all()
    serializer_class = ScheduledEventSerializer
    filterset_class = ScheduledEventFilter


class ScheduledEventView(RetrieveAPIView):
    queryset = ScheduledEvent.objects.all()
    serializer_class = ScheduledEventSerializer
