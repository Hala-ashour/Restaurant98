from rest_framework import serializers
from rest_framework import viewsets
from .models import Category ,Order
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=['id','name','description','is_active']





class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['customer','order_date','total_amount','status','notes']


from rest_framework import serializers
from .models import Customer
from orders.models import Order  # حتى تظهري الطلبات المرتبطة بالعميل

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    orders = OrderSerializer(many=True, read_only=True, source='order_set')

    class Meta:
        model = Customer
        fields = ['id', 'user', 'phone', 'address', 'orders']
