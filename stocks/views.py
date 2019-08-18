from rest_framework import viewsets
from stocks.models import Item, Purchase, Sale
from stocks.serializers import ItemSerializer, PurchaseSerializer, SaleSerializer, SaleByDaySerializer
from stocks.filters import SaleFilter
from django.db.models import Sum, F
from django.db import models


class ItemViewSet(viewsets.ModelViewSet):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()


class PurchaseViewSet(viewsets.ModelViewSet):
    serializer_class = PurchaseSerializer
    queryset = Purchase.objects.all()
    filterset_fields = ['item', 'date']


class SaleViewSet(viewsets.ModelViewSet):
    serializer_class = SaleSerializer
    queryset = Sale.objects.all()
    filter_class = SaleFilter


class SaleByDayViewSet(viewsets.ModelViewSet):
    serializer_class = SaleByDaySerializer
    queryset = Sale.objects.values('date__date').annotate(
        gross=Sum(F('price') * F('qty'), output_field=models.FloatField()),
        cost=Sum(F('purchase__cost') * F('qty'), output_field=models.FloatField()))
    filter_class = SaleFilter
