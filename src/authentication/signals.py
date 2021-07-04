from django.dispatch import receiver
from django.core.mail import send_mail
from friends_gallery.settings import EMAIL_HOST_USER, FRONTEND_URL

from django_rest_passwordreset.signals import reset_password_token_created


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    send_mail(
        subject="Redefine password",
        message=f'Access the link for redefine your password: {FRONTEND_URL}/redefine-password/{reset_password_token.key}',
        from_email=EMAIL_HOST_USER,
        recipient_list=[reset_password_token.user.email],
        fail_silently=True,
    )
