from json import dumps
from django.contrib import admin
from django.template.response import TemplateResponse
from pulsa.models import Provider, Nominal, Transaction
from pulsa.serializers import TransactionSerializer, TransactionByDaySerializer, ProviderSerializers
from rangefilter.filter import DateTimeRangeFilter
from django.db.models import Sum


def cetak_barcode(modeladmin, request, queryset):
    serializer = ProviderSerializers(queryset, many=True)

    context = {
        'providers': dumps(serializer.data),
    }

    return TemplateResponse(request, 'pulsa/template_barcode.html', context)


def tampilkan_laporan(modeladmin, request, queryset):
    serializer = TransactionSerializer(queryset, many=True)
    querysetByDay = Transaction.objects.filter(id__in=queryset).values('date__date').annotate(
        cost=Sum('cost'),
        gross=Sum('price'),
    )
    serializerByDay = TransactionByDaySerializer(querysetByDay, many=True)

    context = {
        'transactions': dumps(serializer.data),
        'transactionsByDay': dumps(serializerByDay.data)
    }

    return TemplateResponse(request, 'pulsa/template_report.html', context)


def custom_titled_filter(title):
    class Wrapper(admin.FieldListFilter):
        def __new__(cls, *args, **kwargs):
            instance = admin.FieldListFilter.create(*args, **kwargs)
            instance.title = title
            return instance
    return Wrapper


class ProviderAdmin(admin.ModelAdmin):
    actions = [cetak_barcode]


class NominalAdmin(admin.ModelAdmin):
    list_display = ('provider', 'nominal', 'Cost', 'Price')

    def nominal(self, nominal):
        return nominal.name

    def Cost(self, nominal):
        return 'Rp{:,.0f}'.format(nominal.cost).replace(',', '.')

    def Price(self, nominal):
        return 'Rp{:,.0f}'.format(nominal.price).replace(',', '.')

    list_per_page = 1000
    list_filter = (
        ('provider__name', custom_titled_filter('provider')),
    )


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('number', 'provider', 'Nominal', 'Cost', 'Price', 'date')

    def provider(self, transaction):
        return transaction.nominal.provider

    def Nominal(self, transaction):
        return transaction.nominal.name

    def Cost(self, transaction):
        return 'Rp{:,.0f}'.format(transaction.cost).replace(',', '.')

    def Price(self, transaction):
        return 'Rp{:,.0f}'.format(transaction.price).replace(',', '.')

    list_filter = (
        ('date', DateTimeRangeFilter),
        ('nominal__provider__name', custom_titled_filter('provider')),
    )
    list_per_page = 1000
    actions = [tampilkan_laporan]


admin.site.register(Provider, ProviderAdmin)
admin.site.register(Nominal, NominalAdmin)
admin.site.register(Transaction, TransactionAdmin)
