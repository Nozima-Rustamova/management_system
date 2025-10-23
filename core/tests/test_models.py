from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


def sample_user(email='user@example.com', password='testpass123', name='Test User'):
    """Create and return a sample user"""
    return get_user_model().objects.create_user(email=email, password=password, name=name)


class ModelTests(TestCase):
    """Test core models"""

    def test_create_teacher_successful(self):
        """Test creating a teacher profile"""
        user = sample_user(email='teacher@example.com', name='Mr. Smith')
        teacher = models.Teacher.objects.create(user=user, subject='Math')
        self.assertEqual(str(teacher), 'Mr. Smith (Math)')

    def test_create_group_successful(self):
        """Test creating a group"""
        user = sample_user(email='teacher@example.com')
        teacher = models.Teacher.objects.create(user=user, subject='Physics')
        group = models.Group.objects.create(name='Physics Group A', teacher=teacher, schedule='Mon-Wed-Fri 10:00 AM')
        self.assertEqual(str(group), 'Physics Group A')

    def test_create_student_and_assign_group(self):
        """Test creating a student and enrolling in group"""
        teacher_user = sample_user(email='teacher@example.com')
        teacher = models.Teacher.objects.create(user=teacher_user, subject='Math')
        group = models.Group.objects.create(name='Math A', teacher=teacher, schedule='Sat 9:00')

        student_user = sample_user(email='student@example.com', name='Alice')
        student = models.Student.objects.create(user=student_user)
        student.enrolled_groups.add(group)

        self.assertIn(group, student.enrolled_groups.all())
        self.assertEqual(str(student), 'Alice')
