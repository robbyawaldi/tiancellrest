from rest_framework import viewsets
from services.serializers import ServiceSerializer
from services.models import Service

class ServiceViewSet(viewsets.ModelViewSet):
    serializer_class = ServiceSerializer
    queryset = Service.objects.all()

