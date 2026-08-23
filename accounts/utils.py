from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail


def send_verification_email(user, request):
    uid=urlsafe_base64_encode(force_bytes(user.pk))
    token=default_token_generator.make_token(user)
    verification_url=request.build_absolute_uri(
        reverse(
            "verify-email",
            kwargs={"uid": uid, "token": token}
        )
    )
    subject="Verify your RemoteHire account"
    message=f"Hi {user.email},\n\nThank you for registering with RemoteHire\n\nPlease click the link below to verify your email address:\n{verification_url}\n\nIf you did not sign up for this account, you can ignore this email.\n\n\nRegards,RemoteHire Team"

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email], 
    )