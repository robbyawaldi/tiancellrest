from django.urls import path, include
from rest_framework.routers import DefaultRouter
from stocks import views

router = DefaultRouter()
router.register(r'items', views.ItemViewSet, base_name='items')
router.register(r'purchases', views.PurchaseViewSet, base_name='purchases')
router.register(r'sales', views.SaleViewSet, base_name='sales')
router.register(r'report', views.SaleByDayViewSet, base_name='report')

urlpatterns = [
    path('', include(router.urls)),
]
