from django.db import models
from django.conf import settings

class Teacher(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='teacher_profile'
    )
    subject = models.CharField(max_length=100)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.name} ({self.subject})"


class Group(models.Model):
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='groups')
    schedule = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Student(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='student_profile'
    )
    enrolled_groups = models.ManyToManyField(Group, related_name='students', blank=True)
    join_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.name
