from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from . import models, serializers

class IsTeacherOrReadOnly(permissions.BasePermission):
    """
    Allow safe methods to any authenticated user.
    Mutating attendance allowed for staff or teachers (simple check).
    You can replace with a real teacher-check later.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return request.user and (request.user.is_staff or hasattr(request.user, 'teacher_profile'))

class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = models.Attendance.objects.all()
    serializer_class = serializers.AttendanceSerializer
    permission_classes = [IsTeacherOrReadOnly]

    def perform_create(self, serializer):
        # mark by current user
        serializer.save(marked_by=self.request.user)

    @action(detail=False, methods=['get'], url_path='by-student/(?P<student_id>[^/.]+)')
    def by_student(self, request, student_id=None):
        qs = self.queryset.filter(student_id=student_id).order_by('-date')
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='by-group/(?P<group_id>[^/.]+)')
    def by_group(self, request, group_id=None):
        qs = self.queryset.filter(group_id=group_id).order_by('-date')
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)
