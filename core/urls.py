from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import TeacherViewSet, GroupViewSet, StudentViewSet

router = DefaultRouter()
router.register('teachers', TeacherViewSet)
router.register('groups', GroupViewSet)
router.register('students', StudentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
