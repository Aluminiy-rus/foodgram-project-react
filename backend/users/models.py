from django.contrib.auth.models import AbstractUser
from django.db import models

USER = "user"
ADMIN = "admin"
ROLES = [
    (USER, "пользователь"),
    (ADMIN, "администратор"),
]


class User(AbstractUser):
    """Модель пользователя."""

    username = models.CharField(
        unique=True,
        max_length=150,
        verbose_name="Имя пользователя",
        db_index=True,
    )
    password = models.CharField(
        max_length=150,
        verbose_name="Пароль",
    )
    email = models.EmailField(
        max_length=254,
        db_index=True,
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name="Имя",
        db_index=True,
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name="Фамилия",
        db_index=True,
    )
    role = models.SlugField(choices=ROLES, default=USER)
    REQUIRED_FIELDS = [
        "password",
        "first_name",
        "last_name",
        "email",
    ]

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == ADMIN or self.is_superuser
