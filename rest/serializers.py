from rest_framework import serializers
from rest_framework import viewsets
from .models import Category
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=['id','name','description','is_active']