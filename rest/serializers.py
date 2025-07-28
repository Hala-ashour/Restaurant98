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


