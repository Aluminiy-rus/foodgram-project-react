from django.core.validators import RegexValidator


class HexColorValidator(RegexValidator):
    """Проверка что цвет указан в формате HEX-кода"""

    regex = r"^#[0-9A-Fa-f]{6}$"
    message = "Значение цвета необходимо указывать в формате HEX-кода!"
