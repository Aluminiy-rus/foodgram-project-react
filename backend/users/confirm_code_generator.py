import uuid

from django.conf import settings
from django.core.mail import send_mail


def confirm_code_generator(user):
    confirmation_code = uuid.uuid4()
    from_email = settings.ADMIN_EMAIL
    to_email = user.email
    send_mail(
        subject="Код подтвеждения регистрации",
        message=f"Код подтвеждения: {confirmation_code}",
        from_email=from_email,
        recipient_list=[to_email],
        fail_silently=False,
    )
