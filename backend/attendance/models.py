from django.db import models
from django.conf import settings
from core import models as core_models

class Attendance(models.Model):
    STATUS_PRESENT = 'P'
    STATUS_ABSENT = 'A'
    STATUS_CHOICES = [
        (STATUS_PRESENT, 'Present'),
        (STATUS_ABSENT,  'Absent'),
    ]

    student = models.ForeignKey(core_models.Student, on_delete=models.CASCADE, related_name='attendances')
    group = models.ForeignKey(core_models.Group, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    marked_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    note = models.TextField(blank=True)

    class Meta:
        unique_together = ('student', 'group', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"{self.date} {self.group.name} {self.student.user.email} {self.get_status_display()}"
