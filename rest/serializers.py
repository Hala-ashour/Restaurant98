from rest_framework import serializers
from rest_framework import viewsets
from .models import Category ,Order, Product,OrderItem

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
        



class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']
        


from rest_framework import serializers
from .models import Customer,Order

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)
    class Meta:
        model = Order
        fields = '__all__'


    
   



    def create(self, validated_data):
            order_items_data = validated_data.pop('order_items')
            order = Order.objects.create(**validated_data)
            for item_data in order_items_data:
                OrderItem.objects.create(order=order, **item_data)
            order.update_total()
            return order

    def update(self, instance, validated_data):
        order_items_data = validated_data.pop('order_items', None)

       
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if order_items_data is not None:
            
            instance.order_items.all().delete()
           
            for item_data in order_items_data:
                OrderItem.objects.create(order=instance, **item_data)

        instance.update_total()
        return instance

    
    

class CustomerSerializer(serializers.ModelSerializer):
    orders = OrderSerializer(many=True, read_only=True, source='order_set')

    class Meta:
        model = Customer
        fields = ['id', 'user', 'phone', 'address', 'orders']
