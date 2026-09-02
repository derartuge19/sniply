from rest_framework import serializers
from .models import Link


class LinkSerializer(serializers.ModelSerializer):
    short_url = serializers.SerializerMethodField()

    class Meta:
        model = Link
        fields = ["id", "short_code", "original_url", "short_url", "is_active", "created_at"]
        read_only_fields = ["id", "short_code", "created_at"]

    def get_short_url(self, obj):
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(f"/{obj.short_code}")
        return f"/{obj.short_code}"