from re import IGNORECASE
from django.core.validators import RegexValidator


class UsernameAllowedValidator(RegexValidator):
    """Валидатор для проверки имени на уровне модели"""

    regex = r"(?!(^me$|^set-password$))^[\w.@+-]+$"
    flags = IGNORECASE
    message = "Недопустимое значение имени."