from rest_framework import serializers


class UsernameAllowedValidator:
    """Валидатор для проверки имени при регистрации"""

    def __init__(self, username):
        self.username = username

    def __call__(self, data):
        if data["username"].lower() == ("me" or "set_password"):
            message = "Недопустимое значение имени"
            raise serializers.ValidationError(message)
        return data


class UserNotAuthorValidator:
    """Валидатор запрещающий подписки на самого себя"""

    def __init__(self, user, following):
        self.user = user
        self.following = following

    def __call__(self, data):
        if data["user"] == data["following"]:
            message = "Подписка на самого себя не возможна."
            raise serializers.ValidationError(message)
        return data
