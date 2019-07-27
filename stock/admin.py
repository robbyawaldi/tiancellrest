import json
from django.template.response import TemplateResponse
from django.contrib import admin
from stock.models import Item, Purchase, Sale
from stock.serializers import PurchaseSerializer

def cetak_qr_code(modeladmin, request, queryset):
    purchases = []
    for i in range(len(queryset)):
        purchase = Purchase.objects.get(id=queryset[i].id)
        serializer = PurchaseSerializer(purchase, context={'request':request})
        purchases.append(serializer.data)

    context = {
        'purchases': json.dumps(purchases),   
    }
    return TemplateResponse(request,'stock/template_qr_code.html', context)

class PurchaseAdmin(admin.ModelAdmin):  
    ordering = ['-date']
    actions = [cetak_qr_code]

admin.site.register(Item)
admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(Sale)
