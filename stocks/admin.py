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
    startDate = queryset[len(queryset) - 1].date
    endDate = queryset[0].date
    querysetByDay = Sale.objects.filter(date__range=[startDate,endDate]).values('date__date').annotate(
        gross=Sum(F('price') * F('qty'), output_field=FloatField()),
        cost=Sum(F('purchase__cost') * F('qty'), output_field=FloatField()))
    serializerByDay = SaleByDaySerializer(querysetByDay, many=True)

    context = {
        'sales': dumps(serializer.data),
        'salesByDay': dumps(serializerByDay.data)
    }

    return TemplateResponse(request, 'stock/template_report.html', context)


class PurchaseAdmin(admin.ModelAdmin):
    ordering = ['-date']
    list_filter = (
        ('date', DateRangeFilter),
        'item__name',
    )
    list_per_page = 1000
    actions = [cetak_barcode]


class SaleAdmin(admin.ModelAdmin):
    ordering = ['-date']
    list_filter = (
        ('date', DateTimeRangeFilter),
        'purchase__item__name',
    )
    list_per_page = 1000
    actions = [tampilkan_laporan]


admin.site.register(Item)
admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(Sale, SaleAdmin)
