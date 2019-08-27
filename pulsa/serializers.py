from rest_framework import serializers
from pulsa.models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'


class TransactionByDaySerializer(serializers.Serializer):
    date = serializers.CharField(source='date__date')
    cost = serializers.FloatField()
    gross = serializers.FloatField()
    net = serializers.SerializerMethodField()

    def get_net(self, transaction):
        return transaction['gross'] - transaction['cost']