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


class RecipeIngredientsValidator:
    """Проверка полей ингредиентов в рецептах"""

    def __init__(self, ingredients):
        self.ingredients = ingredients

    def __call__(self, data):
        ingr_set = list()
        for ingr in data["recipe_ingredient_amount"]:
            if ingr.get("amount") <= 0:
                message = "Ингредиентов должно быть больше 0."
                raise ValidationError(message)
            pk = ingr.get("ingredient")
            ingr_set.append(pk)
            if ingr_set.count(pk) > 1:
                raise ValidationError("Не должено быть повторений.")
        return data


class RecipeCookingTimeValidator:
    """Проверка времени готовки в рецептах"""

    def __init__(self, cooking_time):
        self.cooking_time = cooking_time

    def __call__(self, data):
        if data["cooking_time"] <= 0:
            message = "Время готовки должно быть больше 0."
            raise ValidationError(message)
        return data
