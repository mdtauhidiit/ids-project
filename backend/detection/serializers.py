from rest_framework import serializers

class PacketSerializer(serializers.Serializer):
    duration = serializers.FloatField(required=False, default=0.0)
    src_bytes = serializers.IntegerField(required=False, default=0)
    dst_bytes = serializers.IntegerField(required=False, default=0)
    failed_logins = serializers.IntegerField(required=False, default=0)
    same_srv_rate = serializers.FloatField(required=False, default=1.0)
    serror_rate = serializers.FloatField(required=False, default=0.0)
    flag = serializers.CharField(required=False, default="SF", max_length=10)
    payload = serializers.CharField(required=False, default="", allow_blank=True)