from django.urls import path, include
from rest_framework.routers import DefaultRouter
from stocks.views import ItemViewSet, PurchaseViewSet, SaleViewSet

router = DefaultRouter()
router.register(r'items', ItemViewSet)
router.register(r'purchases', PurchaseViewSet)
router.register(r'sales', SaleViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
