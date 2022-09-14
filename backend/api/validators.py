from rest_framework import serializers


class UsernameNotMeValidator:
    """Валидатор для проверки имени при регистрации"""

    def __init__(self, username):
        self.username = username

    def __call__(self, data):
        if data["username"].lower() == "me":
            message = "Использовать 'me' в качестве имени запрещено"
            raise serializers.ValidationError(message)
        return data
