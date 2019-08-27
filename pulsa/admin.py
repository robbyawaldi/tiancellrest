from json import dumps
from django.contrib import admin
from django.template.response import TemplateResponse
from pulsa.models import Provider, Nominal, Transaction
from pulsa.serializers import TransactionSerializer, TransactionByDaySerializer
from rangefilter.filter import DateTimeRangeFilter
from django.db.models import Sum

def tampilkan_laporan(modeladmin, request, queryset):
    serializer = TransactionSerializer(queryset, many=True)
    startDate = queryset[len(queryset) - 1].date
    endDate = queryset[0].date
    querysetByDay = Transaction.objects.filter(date__range=[startDate, endDate]).values('date__date').annotate(
        cost=Sum('cost'),
        gross=Sum('price'),
    )
    serializerByDay = TransactionByDaySerializer(querysetByDay, many=True)

    context = {
        'transactions': dumps(serializer.data),
        'transactionsByDay': dumps(serializerByDay.data)
    }

    return TemplateResponse(request, 'pulsa/template_report.html', context)

class TransactionAdmin(admin.ModelAdmin):
    ordering = ['-date']
    list_filter = (
        ('date', DateTimeRangeFilter),
    )
    list_per_page = 1000
    actions = [tampilkan_laporan]

admin.site.register(Provider)
admin.site.register(Nominal)
admin.site.register(Transaction, TransactionAdmin)
