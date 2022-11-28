from rest_framework import serializers

from src.mextalki.models import Teacher


class TeacherSerializer(serializers.ModelSerializer):
    time_zone = serializers.SerializerMethodField()

    def get_time_zone(self, obj):
        return str(obj.time_zone)

    class Meta:
        model = Teacher
        fields = (
            'id',
            'name',
            'active',
            'time_zone',
        )
