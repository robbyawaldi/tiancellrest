from rest_framework import serializers
from stocks.models import Item, Purchase, Sale


class ItemSerializer(serializers.ModelSerializer):
    stock = serializers.SerializerMethodField()
    currentpurchase = serializers.SerializerMethodField()

    def get_stock(self, item):
        return item.stock()

    def get_currentpurchase(self, item):
        return item.currentpurchase()

    class Meta:
        model = Item
        fields = ('id', 'name', 'price', 'stock', 'currentpurchase')


class PurchaseSerializer(serializers.ModelSerializer):
    item_name = serializers.SerializerMethodField()
    sold = serializers.SerializerMethodField()
    remaining = serializers.SerializerMethodField()

    def get_item_name(self, purchase):
        return purchase.item_name()

    def get_sold(self, purchase):
        return purchase.sold()

    def get_remaining(self, purchase):
        return purchase.remaining()

    class Meta:
        model = Purchase
        fields = ('id', 'item','item_name', 'cost', 'qty', 'sold', 'remaining', 'date')


class SaleSerializer(serializers.ModelSerializer):
    item_name = serializers.SerializerMethodField(read_only=True)

    def get_item_name(self, sale):
        if isinstance(sale, dict):
            return sale['purchase'].item_name()
        else:
            return sale.purchase.item_name()
            

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
        fields = ('id', 'purchase', 'item_name', 'price', 'qty', 'date')


class SaleByDaySerializer(serializers.Serializer):
    date = serializers.CharField(source='date__date')
    cost = serializers.FloatField()
    gross = serializers.FloatField()
    net = serializers.SerializerMethodField()

    def get_net(self, sale):
        return sale['gross'] - sale['cost']
