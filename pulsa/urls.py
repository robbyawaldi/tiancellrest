from django.urls import path, include
from rest_framework.routers import DefaultRouter
from pulsa import views

router = DefaultRouter()
router.register(r'providers', views.ProviderViewSet, base_name='providers')
router.register(r'nominals', views.NominalViewSet, base_name='nominals')
router.register(r'transactions', views.TransactionViewSet, base_name='transactions')
router.register(r'latest_transactions', views.LatestTransactionViewSet, base_name='latest_transactions')

urlpatterns = [
    path('', include(router.urls)),
]