from django.contrib import admin
from pulsa.models import Provider, Nominal, Transaction

admin.site.register(Provider)
admin.site.register(Nominal)
admin.site.register(Transaction)
