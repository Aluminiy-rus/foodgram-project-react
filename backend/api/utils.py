import base64

import webcolors
from django.core.files.base import ContentFile
from rest_framework import serializers


def get_is_subscribed(self, obj):
    """Проверка статуса подписки"""
    user = self.context["request"].user
    return (
        user.is_authenticated and user.follow_user.filter(author=obj).exists()
    )


class Hex2NameColor(serializers.Field):
    """Hex-color в читабельный вид"""

    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        try:
            data = webcolors.hex_to_name(data)
        except ValueError:
            raise serializers.ValidationError("Для этого цвета нет имени")


class Base64ImageField(serializers.ImageField):
    """Декодер картринки из формата Base64"""

    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith("data:image"):
            format, imgstr = data.split(";base64,")
            ext = format.split("/")[-1]
            data = ContentFile(base64.b64decode(imgstr), name="temp." + ext)
        return super().to_internal_value(data)
