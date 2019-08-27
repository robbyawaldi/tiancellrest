from rest_framework import serializers
from services.models import Service

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'


class ServiceByDaySerializer(serializers.Serializer):
    date = serializers.CharField(source='date__date')
    cost = serializers.FloatField()
    gross = serializers.FloatField()
    net = serializers.SerializerMethodField()

    def get_net(self, service):
        return service['gross'] - service['cost']