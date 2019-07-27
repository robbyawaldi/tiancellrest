from rest_framework import serializers
from stock.models import Item, Purchase, Sale


class ItemSerializer(serializers.HyperlinkedModelSerializer):
    purchases = serializers.SerializerMethodField()

    def get_purchases(self, item):
        queryset = Purchase.objects.filter(item=item).order_by('date')
        purchases_id = [p.id for p in queryset if not p.stock_out()]
        queryset = Purchase.objects.filter(id__in=purchases_id)
        serializer = PurchaseItemSerializer(
            queryset, many=True, context=self.context)
        return serializer.data

    class Meta:
        model = Item
        fields = ('url', 'id', 'name', 'price', 'purchases')

class PurchaseItemSerializer(serializers.HyperlinkedModelSerializer):
    sold = serializers.SerializerMethodField()

    def get_sold(self, obj):
        return obj.sold()

    class Meta:
        model = Purchase
        fields = ('url', 'qty', 'sold')


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
