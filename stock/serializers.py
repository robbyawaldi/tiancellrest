from rest_framework import serializers
from stock.models import Item, Purchase, Sale


class ItemSerializer(serializers.HyperlinkedModelSerializer):
    stock = serializers.SerializerMethodField()

    def get_stock(self, item):
        return item.stock()

    class Meta:
        model = Item
        fields = ('url', 'id', 'name', 'price', 'stock')


class PurchaseSerializer(serializers.HyperlinkedModelSerializer):
    sales = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='sale-detail'
    )
    item_name = serializers.SerializerMethodField()
    stock_out = serializers.SerializerMethodField()
        
    def get_item_name(self, purchase):
        return purchase.item.name

    def get_stock_out(self, purchase):
        return purchase.stock_out()

    class Meta:
        model = Purchase
        fields = ('url', 'id', 'item','item_name', 'cost', 'qty',
                  'date', 'sales', 'stock_out')


class SaleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Sale
        fields = ('url', 'id', 'purchase', 'price', 'qty', 'date')
