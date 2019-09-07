from json import dumps
from django.template.response import TemplateResponse
from django.contrib import admin
from rangefilter.filter import DateTimeRangeFilter, DateRangeFilter
from stocks.models import Item, Purchase, Sale
from stocks.serializers import PurchaseSerializer, SaleSerializer, SaleByDaySerializer
from django.db.models import Sum, F, FloatField


def cetak_barcode(modeladmin, request, queryset):
    serializer = PurchaseSerializer(queryset, many=True)

    context = {
        'purchases': dumps(serializer.data),
    }

    return TemplateResponse(request, 'stock/template_barcode.html', context)


def tampilkan_laporan(modeladmin, request, queryset):
    serializer = SaleSerializer(queryset, many=True)
    querysetByDay = Sale.objects.filter(id__in=queryset).values('date__date').annotate(
        gross=Sum(F('price') * F('qty'), output_field=FloatField()),
        cost=Sum(F('purchase__cost') * F('qty'), output_field=FloatField()))
    serializerByDay = SaleByDaySerializer(querysetByDay, many=True)

    context = {
        'sales': dumps(serializer.data),
        'salesByDay': dumps(serializerByDay.data)
    }

    return TemplateResponse(request, 'stock/template_report.html', context)


def custom_titled_filter(title):
    class Wrapper(admin.FieldListFilter):
        def __new__(cls, *args, **kwargs):
            instance = admin.FieldListFilter.create(*args, **kwargs)
            instance.title = title
            return instance
    return Wrapper


class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'Price', 'stock')

    def Price(self, item):
        return 'Rp{:,.0f}'.format(item.price).replace(',', '.')

    def stock(self, item):
        return item.stock()


class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('item_name', 'Cost', 'qty', 'date')

    def Cost(self, purchase):
        return 'Rp{:,.0f}'.format(purchase.cost).replace(',', '.')

    def item_name(self, purchase):
        return purchase.item_name()

    list_filter = (
        ('date', DateRangeFilter),
        ('date', custom_titled_filter('group date')),
        'item__name',
    )
    list_per_page = 1000
    actions = [cetak_barcode]


class SaleAdmin(admin.ModelAdmin):
    list_display = ('name', 'Price', 'qty', 'date')

    def name(self, sale):
        return sale.purchase.item_name()

    def Price(self, sale):
        return 'Rp{:,.0f}'.format(sale.price).replace(',', '.')

    list_filter = (
        ('date', DateTimeRangeFilter),
        'purchase__item__name',
    )
    list_per_page = 1000
    actions = [tampilkan_laporan]


admin.site.register(Item, ItemAdmin)
admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(Sale, SaleAdmin)
