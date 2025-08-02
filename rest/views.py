from django.shortcuts import render
from .serializers import CategorySerializer,OrderSerializer, ProductSerializer
from .models import Category,Order, Product
from rest_framework import viewsets,status
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminOrReadOnly


from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from django_filters import rest_framework as filters

class ProductFilter(filters.FilterSet):
    price_lt = filters.NumberFilter(field_name='price', lookup_expr='lt')
    price_gt = filters.NumberFilter(field_name='price', lookup_expr='gt')
    price_lte = filters.NumberFilter(field_name='price', lookup_expr='lte')
    price_gte = filters.NumberFilter(field_name='price', lookup_expr='gte')

    class Meta:
        model = Product
        fields = ['category', 'is_available']



class IsAdminOrManager(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:  
            return True
        return request.user.is_authenticated and (
            request.user.is_staff or getattr(request.user, 'role', '') == 'manager'
        )
    
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminOrManager()]

        return [IsAuthenticated()]  





class OrderPagination(PageNumberPagination):
    page_size = 5

class OrderViewset(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = OrderPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'customer']





from rest_framework import viewsets
from .models import Customer
from .serializers import CustomerSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]




    @action(detail=True, methods=['get'])
    def orders(self, request, pk=None):
        customer = self.get_object()
        orders = customer.order_set.all()  
        data = OrderSerializer(orders, many=True).data
        return Response(data)
    

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter
    pagination_class = PageNumberPagination

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
           return [IsAdminOrManager()]

        return [IsAuthenticated()]  
    
    @action(detail=True, methods=['GET'], url_path='check-availability')
    def check_availability(self, request, pk=None):
        
        product = self.get_object()
        return Response({
            'product_id': product.id,
            'product_name': product.name,
            'is_available': product.is_available,
            'message': 'Available for order' if product.is_available else 'Currently unavailable'
        }, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['GET'], url_path='available')
    def available_products(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        
        available_products = queryset.filter(is_available=True)
        
        page = self.paginate_queryset(available_products)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(available_products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['GET'], url_path='menu-by-category')
    def menu_by_category(self, request):
        
        categories = Category.objects.filter(is_active=True).prefetch_related('products')
        
        result = []
        for category in categories:
            products = category.products.filter(is_available=True)
            if products.exists():  # Only include categories with available products
                serializer = ProductSerializer(products, many=True)
                result.append({
                    'category_id': category.id,
                    'category_name': category.name,
                    'category_description': category.description,
                    'products': serializer.data
                })
        
        return Response(result, status=status.HTTP_200_OK)


