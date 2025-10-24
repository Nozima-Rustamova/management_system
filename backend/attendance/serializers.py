from rest_framework import serializers
from . import models

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Attendance
        fields = ['id', 'student', 'group', 'date', 'status', 'marked_by', 'note']
        read_only_fields = ['marked_by']

    def validate(self, attrs):
        # ensure student belongs to the group (optional safety check)
        student = attrs.get('student')
        group = attrs.get('group')
        if student and group:
            if not student.enrolled_groups.filter(pk=group.pk).exists():
                raise serializers.ValidationError("Student is not enrolled in this group.")
        return attrs
