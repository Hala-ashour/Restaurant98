from django.shortcuts import render
from .serializers import CategorySerializer,OrderSerializer
from .models import Category,Order
from rest_framework import viewsets,status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination



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

class orderviewset(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = OrderPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'customer']