from rest_framework.serializers import ValidationError


class UsernameAllowedValidator:
    """Валидатор для проверки имени при регистрации"""

    def __init__(self, username):
        self.username = username

    def __call__(self, data):
        if data["username"].lower() == ("me" or "set_password"):
            message = "Недопустимое значение имени"
            raise ValidationError(message)
        return data


class UserNotAuthorValidator:
    """Валидатор запрещающий подписки на самого себя"""

    def __init__(self, user, author):
        self.user = user
        self.author = author

    def __call__(self, data):
        if data["user"] == data["author"]:
            message = "Подписка на самого себя не возможна."
            raise ValidationError(message)
        return data


class RecipeIngredientsAmountValidator:
    """Проверка полей ингредиентов в рецептах"""

    def __init__(self, amount):
        self.amount = amount

    def __call__(self, data):
        if data["amount"] <= 0:
            message = "Ингредиентов должно быть больше 0."
            raise ValidationError(message)
        return data

