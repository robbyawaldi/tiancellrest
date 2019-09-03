from rest_framework import serializers
from pulsa.models import Transaction, Nominal, Provider


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'


class NominalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nominal
        fields = ('id', 'name', 'cost', 'price')


class ProviderSerializers(serializers.ModelSerializer):
    nominals = NominalSerializer(many=True, read_only=True)

    class Meta:
        model = Provider
        fields = ('name', 'nominals')


class TransactionByDaySerializer(serializers.Serializer):
    date = serializers.CharField(source='date__date')
    cost = serializers.FloatField()
    gross = serializers.FloatField()
    net = serializers.SerializerMethodField()

    def get_net(self, transaction):
        return transaction['gross'] - transaction['cost']
