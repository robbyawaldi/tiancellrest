from json import dumps
from django.template.response import TemplateResponse
from django.contrib import admin
from django.db.models import Sum
from services.models import Service
from services.serializers import ServiceSerializer, ServiceByDaySerializer
from rangefilter.filter import DateTimeRangeFilter


def tampilkan_laporan(modeladmin, request, queryset):
    serializer = ServiceSerializer(queryset, many=True)
    querysetByDay = Service.objects.filter(id__in=queryset).values('date__date').annotate(
        cost=Sum('cost'),
        gross=Sum('price'),
    )
    serializerByDay = ServiceByDaySerializer(querysetByDay, many=True)

    context = {
        'services': dumps(serializer.data),
        'servicesByDay': dumps(serializerByDay.data)
    }

    return TemplateResponse(request, 'services/template_report.html', context)


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('brand', 'type', 'Cost', 'Price', 'date')

    def Cost(self, service):
        return 'Rp{:,.0f}'.format(service.cost).replace(',', '.')

    def Price(self, service):
        return 'Rp{:,.0f}'.format(service.price).replace(',', '.')

    ordering = ['-date']
    list_filter = (
        ('date', DateTimeRangeFilter),
    )
    list_per_page = 1000
    actions = [tampilkan_laporan]


admin.site.register(Service, ServiceAdmin)
