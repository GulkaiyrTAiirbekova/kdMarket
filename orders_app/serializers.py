from rest_framework import serializers
from orders_app.models import Order, OrderItem


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model= Order
        fields = '__all__'
class OrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem ##закзанный товар
        fields = '__all__'


