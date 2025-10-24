from django.contrib.auth import get_user_model
from rest_framework import serializers

from . import models


class TeacherSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.all()
    )

    class Meta:
        model = models.Teacher
        fields = ['id', 'user', 'subject', 'bio']


class GroupSerializer(serializers.ModelSerializer):
    teacher = serializers.PrimaryKeyRelatedField(
        queryset=models.Teacher.objects.all()
    )

    class Meta:
        model = models.Group
        fields = ['id', 'name', 'teacher', 'schedule']


class StudentSerializer(serializers.ModelSerializer):
    # For simplicity we expose user by PK and enrolled_groups by PKs.
    user = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.all()
    )
    enrolled_groups = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=models.Group.objects.all(),
        required=False
    )

    class Meta:
        model = models.Student
        fields = ['id', 'user', 'enrolled_groups', 'join_date']
        read_only_fields = ['join_date']
