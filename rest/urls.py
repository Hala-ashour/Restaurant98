from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet,orderviewset

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')


urlpatterns = [
    path('', include(router.urls)),
]



router = DefaultRouter()
router.register('Orders/', orderviewset)


urlpatterns = router.urls




from .views import CustomerViewSet

router = DefaultRouter()
router.register(r'customers', CustomerViewSet, basename='customer')

urlpatterns = [
    path('', include(router.urls)),
]
