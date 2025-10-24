from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'student', 'group', 'amount', 'method', 'note', 'paid_at', 'recorded_by']
        read_only_fields = ['paid_at', 'recorded_by']

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value
