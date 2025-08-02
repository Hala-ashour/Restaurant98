from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ProductViewSet,CustomerViewSet

from .views import OrderViewset

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'customers', CustomerViewSet, basename='customer')

router.register('Orders/', OrderViewset)

urlpatterns = [
    path('', include(router.urls)),
]

urlpatterns = router.urls

