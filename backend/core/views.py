from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from . import models
from .serializers import TeacherSerializer, GroupSerializer, StudentSerializer


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Simple permission: safe methods allowed for authenticated users.
    Unsafe methods allowed only for staff/superuser.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return request.user and request.user.is_staff


class TeacherViewSet(viewsets.ModelViewSet):
    queryset = models.Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [IsAdminOrReadOnly]


class GroupViewSet(viewsets.ModelViewSet):
    queryset = models.Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAdminOrReadOnly]


class StudentViewSet(viewsets.ModelViewSet):
    queryset = models.Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """
        If the creator omits the `user` field, attach the request.user.
        This makes it easy for a student user to create their Student profile.
        """
        user = serializer.validated_data.get('user', None)
        if user is None and self.request.user and self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            serializer.save()

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def enroll(self, request, pk=None):
        """
        Enroll the student (pk) into groups sent in body { "groups": [1,2] }.
        """
        student = self.get_object()
        group_ids = request.data.get('groups', [])
        if not isinstance(group_ids, (list, tuple)):
            return Response({"detail": "groups must be a list of ids"}, status=status.HTTP_400_BAD_REQUEST)
        groups = models.Group.objects.filter(id__in=group_ids)
        student.enrolled_groups.add(*groups)
        return Response({'detail': 'enrolled', 'count': groups.count()}, status=status.HTTP_200_OK)

