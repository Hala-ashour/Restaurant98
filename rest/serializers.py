from rest_framework import serializers
from rest_framework import viewsets
from .models import Category ,Order, Product

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=['id','name','description','is_active']


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id', 
            'name', 
            'description', 
            'price', 
            'category', 
            'category_name',
            'is_available', 
            'preparation_time',
            'created_at',
            'updated_at'
        ]
        extra_kwargs = {
            'category': {'write_only': True}
        }
        


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['customer','order_date','total_amount','status','notes']


from rest_framework import serializers
from .models import Customer,Order
# from orders.models import   # حتى تظهري الطلبات المرتبطة بالعميل

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    orders = OrderSerializer(many=True, read_only=True, source='order_set')

    class Meta:
        model = Customer
        fields = ['id', 'user', 'phone', 'address', 'orders']
