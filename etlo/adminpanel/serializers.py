from rest_framework import serializers
from django.contrib.auth.models import User

class RejectSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    message = serializers.CharField()


class HealthInsuranceSubmitSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()
    insurance_number = serializers.CharField()
    file = serializers.FileField()


class ChargeWalletSerializer(serializers.Serializer):
    user = serializers.IntegerField()
    currency = serializers.IntegerField()
    amount = serializers.FloatField()
    bank_code = serializers.CharField()
    details = serializers.CharField()
