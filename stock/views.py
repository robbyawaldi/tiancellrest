from django.urls import reverse_lazy
from django.views.generic import ListView
from rest_framework import viewsets
from stock.models import Item, Purchase, Sale
from stock.serializers import ItemSerializer, PurchaseSerializer, SaleSerializer


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class PurchaseViewSet(viewsets.ModelViewSet):
    queryset = Purchase.objects.all().order_by('-date')
    serializer_class = PurchaseSerializer
    filterset_fields = ['date', 'item']


class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
