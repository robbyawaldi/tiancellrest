import json
from django.template.response import TemplateResponse
from django.contrib import admin
from rangefilter.filter import DateTimeRangeFilter, DateRangeFilter
from stocks.models import Item, Purchase, Sale
from stocks.serializers import PurchaseSerializer


def cetak_barcode(modeladmin, request, queryset):
    purchases = []
    for i in range(len(queryset)):
        purchase = Purchase.objects.get(id=queryset[i].id)
        serializer = PurchaseSerializer(purchase, context={'request': request})
        purchases.append(serializer.data)

    context = {
        'purchases': json.dumps(purchases),
    }
    return TemplateResponse(request, 'stock/template_barcode.html', context)


class PurchaseAdmin(admin.ModelAdmin):
    ordering = ['-date']
    list_filter = (
        ('date', DateRangeFilter),
        'item__name',
    )
    list_per_page = 1000
    actions = [cetak_barcode]


class SaleAdmin(admin.ModelAdmin):
    list_filter = (
        ('date', DateTimeRangeFilter),
        'purchase__item__name',
    )
    list_per_page = 1000


admin.site.register(Item)
admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(Sale, SaleAdmin)
