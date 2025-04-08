from rest_framework import serializers


class PhonenumberInfo(serializers.Serializer):
    provider = serializers.CharField(source='provider.name')
    region = serializers.CharField(source='city.region.name')
    city = serializers.CharField(source='city.name')
