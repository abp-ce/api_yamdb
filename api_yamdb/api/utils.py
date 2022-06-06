from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail


def send_confirmation_code(user):
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        subject='Confirmation code',
        message=confirmation_code,
        from_email='fake@yamdb.fake',
        recipient_list=[user.email]
    )
    return confirmation_code
