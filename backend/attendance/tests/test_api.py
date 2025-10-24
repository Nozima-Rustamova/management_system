from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from core import models as core_models
from django.contrib.auth import get_user_model
from django.urls import reverse
from datetime import date

ATT_URL = reverse('attendance:attendance-list')  # via DefaultRouter

def sample_user(email='s@example.com', password='pass'):
    return get_user_model().objects.create_user(email=email, password=password, name='Name')

class AttendanceApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.teacher_user = sample_user(email='t@example.com', password='pass')
        core_models.Teacher.objects.create(user=self.teacher_user, subject='Math')
        self.group = core_models.Group.objects.create(name='G1', teacher=core_models.Teacher.objects.first(), schedule='Mon')
        self.student_user = sample_user(email='stu@example.com')
        self.student = core_models.Student.objects.create(user=self.student_user)
        self.student.enrolled_groups.add(self.group)
        # authenticate as teacher
        self.client.force_authenticate(user=self.teacher_user)

    def test_mark_attendance(self):
        payload = {'student': self.student.id, 'group': self.group.id, 'date': date.today().isoformat(), 'status': 'P'}
        res = self.client.post(ATT_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['status'], 'P')

    def test_cant_enroll_unrelated_student(self):
        # create another group and ensure validation rejects incorrect student-group
        other_teacher = sample_user(email='t2@example.com')
        core_models.Teacher.objects.create(user=other_teacher, subject='Eng')
        other_group = core_models.Group.objects.create(name='G2', teacher=core_models.Teacher.objects.last(), schedule='Tue')
        payload = {'student': self.student.id, 'group': other_group.id, 'date': date.today().isoformat(), 'status': 'P'}
        res = self.client.post(ATT_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
