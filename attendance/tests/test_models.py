from django.test import TestCase
from core import models as core_models
from attendance import models as att_models
from django.contrib.auth import get_user_model
from datetime import date

def sample_user(email='s@example.com', password='pass'):
    return get_user_model().objects.create_user(email=email, password=password, name='Name')

class AttendanceModelTests(TestCase):
    def setUp(self):
        self.teacher_user = sample_user(email='t@example.com')
        self.teacher = core_models.Teacher.objects.create(user=self.teacher_user, subject='Math')
        self.group = core_models.Group.objects.create(name='G1', teacher=self.teacher, schedule='Mon')
        self.student_user = sample_user(email='stu@example.com')
        self.student = core_models.Student.objects.create(user=self.student_user)
        self.student.enrolled_groups.add(self.group)

    def test_create_attendance(self):
        att = att_models.Attendance.objects.create(student=self.student, group=self.group, date=date.today(), status='P', marked_by=self.teacher_user)
        self.assertEqual(str(att).split()[1], self.group.name)
