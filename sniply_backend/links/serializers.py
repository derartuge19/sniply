from rest_framework import serializers
from .models import Link


from rest_framework import serializers
from .models import Link


class LinkSerializer(serializers.ModelSerializer):
    short_url = serializers.SerializerMethodField()

    class Meta:
        model = Link
        fields = ["id", "short_code", "original_url", "short_url", "custom_domain", "is_active", "created_at"]
        read_only_fields = ["id", "short_code", "created_at"]

    def get_short_url(self, obj):
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(f"/{obj.short_code}")
        return f"/{obj.short_code}"

    def validate_custom_domain(self, value):
        request = self.context.get("request")
        user = request.user

        try:
            is_pro = user.subscription.plan.name == "Pro"
        except AttributeError:
            is_pro = False

        if value and not is_pro:
            raise serializers.ValidationError("Custom domains are a Pro feature. Upgrade to use this.")

        return value


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