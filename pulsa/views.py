from rest_framework import viewsets
from pulsa.serializers import ProviderSerializers, NominalSerializer, TransactionSerializer
from pulsa.models import Provider, Nominal, Transaction

class ProviderViewSet(viewsets.ModelViewSet):
    serializer_class = ProviderSerializers
    queryset = Provider.objects.all()


class NominalViewSet(viewsets.ModelViewSet):
    serializer_class = NominalSerializer
    queryset = Nominal.objects.all()


class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()