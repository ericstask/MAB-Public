from rest_framework import serializers
from .models import Audit, AuditType


class AuditTypeSerializer(serializers.ModelSerializer):
    frequency = serializers.CharField(source='get_testing_frequency_display', read_only=True)

    class Meta:
        model = AuditType
        fields = '__all__'


class AuditSerializer(serializers.ModelSerializer):
    client_value = serializers.CharField(source='get_client_display', read_only=True)
    audit_type = AuditTypeSerializer()

    class Meta:
        model = Audit
        fields = '__all__'