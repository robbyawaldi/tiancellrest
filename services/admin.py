from json import dumps
from django.template.response import TemplateResponse
from django.contrib import admin
from django.db.models import Sum
from services.models import Service
from services.serializers import ServiceSerializer, ServiceByDaySerializer
from rangefilter.filter import DateTimeRangeFilter

def tampilkan_laporan(modeladmin, request, queryset):
    serializer = ServiceSerializer(queryset, many=True)
    startDate = queryset[len(queryset) - 1].date
    endDate = queryset[0].date
    querysetByDay = Service.objects.filter(date__range=[startDate, endDate]).values('date__date').annotate(
        cost=Sum('cost'),
        gross=Sum('price'),
    )
    serializerByDay = ServiceByDaySerializer(querysetByDay, many=True)

    context = {
        'services': dumps(serializer.data),
        'servicesByDay' : dumps(serializerByDay.data)
    }

    return TemplateResponse(request, 'services/template_report.html', context)

class ServiceAdmin(admin.ModelAdmin):
    ordering = ['-date']
    list_filter = (
        ('date', DateTimeRangeFilter),
    )
    list_per_page = 1000
    actions = [tampilkan_laporan]

admin.site.register(Service, ServiceAdmin)

