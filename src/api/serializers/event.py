from rest_framework import serializers

from src.api.serializers.event_type import EvenTypeSerializer
from src.api.serializers.teacher import TeacherSerializer
from src.api.serializers.user import UserSerializer
from src.mextalki.models import ScheduledEvent


class ScheduledEventSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer(many=False)
    user = UserSerializer(many=False)
    event_type = EvenTypeSerializer(many=False)
    time_zone = serializers.SerializerMethodField()

    def get_time_zone(self, obj):
        return str(obj.time_zone)

    class Meta:
        model = ScheduledEvent
        fields = (
            'id',
            'start_time',
            'end_time',
            'provider',
            'provider_event_id',
            'provider_invite_id',
            'user',
            'teacher',
            'event_type',
            'location',
            'status',
            'time_zone',
        )
