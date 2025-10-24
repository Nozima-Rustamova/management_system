from django.db import models
from django.conf import settings
from core import models as core_models

class Payment(models.Model):
    METHOD_CASH = 'cash'
    METHOD_CARD = 'card'
    METHOD_ONLINE = 'online'

    METHOD_CHOICES = [
        (METHOD_CASH, 'Cash'),
        (METHOD_CARD, 'Card'),
        (METHOD_ONLINE, 'Online'),
    ]

    student = models.ForeignKey(core_models.Student, on_delete=models.CASCADE, related_name='payments')
    group = models.ForeignKey(core_models.Group, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=20, choices=METHOD_CHOICES, default=METHOD_CASH)
    paid_at = models.DateTimeField(auto_now_add=True)
    note = models.TextField(blank=True)
    recorded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['-paid_at']

    def __str__(self):
        return f"{self.student.user.email} paid {self.amount} for {self.group.name}"
