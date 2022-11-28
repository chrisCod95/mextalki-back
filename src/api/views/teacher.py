from rest_framework import generics

from src.api.serializers.teacher import TeacherSerializer
from src.mextalki.models import Teacher


class TeacherListView(
    generics.ListAPIView,
):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    filterset_fields = ['active']
