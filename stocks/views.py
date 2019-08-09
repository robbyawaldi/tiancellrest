from rest_framework import viewsets
from stocks.models import Item, Purchase, Sale
from stocks.serializers import ItemSerializer, PurchaseSerializer, SaleSerializer


class ItemViewSet(viewsets.ModelViewSet):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()


class PurchaseViewSet(viewsets.ModelViewSet):
    serializer_class = PurchaseSerializer
    queryset = Purchase.objects.all()
    filterset_fields = ['item','date']

class SaleViewSet(viewsets.ModelViewSet):
    serializer_class = SaleSerializer
    queryset = Sale.objects.all()
