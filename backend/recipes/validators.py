from django.core.validators import RegexValidator

hex_color_validator = RegexValidator(
    regex=r"^[A-Fa-f0-9]{6}$", message=("Введите валидный цветовой HEX-код!")
)
