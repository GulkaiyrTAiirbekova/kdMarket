from rest_framework import serializers
from .models import Payment
from .models import PaymentItem


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields ='__all__'



class PaymentItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentItem