from rest_framework import serializers
from stock.models import Item, Purchase, Sale


class ItemSerializer(serializers.ModelSerializer):
    stock = serializers.SerializerMethodField()
    currentpurchase = serializers.SerializerMethodField()

    def get_stock(self, item):
        return item.stock()

    def get_currentpurchase(self, item):
        return item.purchases()[0].id if item.stock() else None

    class Meta:
        model = Item
        fields = ('id', 'name', 'price', 'stock', 'currentpurchase')


class PurchaseSerializer(serializers.ModelSerializer):
    sold = serializers.SerializerMethodField()
    remaining = serializers.SerializerMethodField()

    def get_sold(self, purchase):
        return purchase.sold()

    def get_remaining(self, purchase):
        return purchase.remaining()

    class Meta:
        model = Purchase
        fields = ('id', 'item', 'cost', 'qty', 'sold', 'remaining', 'date')


class SaleSerializer(serializers.ModelSerializer):

    def create(self, sale):
        purchase = sale['purchase']
        if sale['qty'] <= purchase.remaining():
            Sale.objects.create(**sale)
        else:
            remaining = sale['qty'] - purchase.remaining()
            sale['qty'] = purchase.remaining()
            Sale.objects.create(**sale)
            sale['qty'] = remaining
            sale['purchase'] = purchase.item.purchases()[0]
            self.create(sale)
        return sale

    class Meta:
        model = Sale
        fields = ('id', 'purchase', 'price', 'qty', 'date')
