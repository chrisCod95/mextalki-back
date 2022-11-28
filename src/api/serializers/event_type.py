from rest_framework import serializers

from src.mextalki.models import EventType


class EvenTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventType
        fields = (
            'id',
            'title',
            'active',
            'is_conversation_club',
        )
