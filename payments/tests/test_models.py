from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models as core_models
from payments import models as pay_models

def sample_user(email='user@example.com', password='pass123'):
    return get_user_model().objects.create_user(email=email, password=password, name='Name')

class PaymentModelTests(TestCase):
    def setUp(self):
        self.user = sample_user()
        self.teacher = core_models.Teacher.objects.create(user=self.user, subject='Math')
        self.group = core_models.Group.objects.create(name='Group1', teacher=self.teacher, schedule='Mon')
        self.student_user = sample_user(email='stu@example.com')
        self.student = core_models.Student.objects.create(user=self.student_user)
        self.student.enrolled_groups.add(self.group)

    def test_create_payment(self):
        payment = pay_models.Payment.objects.create(
            student=self.student,
            group=self.group,
            amount=200.00,
            method='cash',
            recorded_by=self.user,
        )
        self.assertEqual(str(payment), f"{self.student.user.email} paid 200.00 for {self.group.name}")
