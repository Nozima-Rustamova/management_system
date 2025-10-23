from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from django.urls import reverse
from core import models as core_models

PAYMENT_URL = reverse('payments:payment-list')

def sample_user(email='user@example.com', password='pass123'):
    return get_user_model().objects.create_user(email=email, password=password, name='Name')

class PaymentApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = sample_user()
        self.client.force_authenticate(self.user)
        self.teacher = core_models.Teacher.objects.create(user=self.user, subject='Math')
        self.group = core_models.Group.objects.create(name='Group1', teacher=self.teacher, schedule='Mon')
        self.student_user = sample_user(email='stu@example.com')
        self.student = core_models.Student.objects.create(user=self.student_user)
        self.student.enrolled_groups.add(self.group)

    def test_create_payment(self):
        payload = {
            'student': self.student.id,
            'group': self.group.id,
            'amount': 250.00,
            'method': 'cash'
        }
        res = self.client.post(PAYMENT_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(float(res.data['amount']), 250.00)
        self.assertEqual(res.data['method'], 'cash')

    def test_invalid_amount_rejected(self):
        payload = {
            'student': self.student.id,
            'group': self.group.id,
            'amount': -50,
            'method': 'card'
        }
        res = self.client.post(PAYMENT_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
