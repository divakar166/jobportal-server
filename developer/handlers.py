from django.dispatch import receiver
from .signals import developer_registered
from .utils import send_verification_email  # Adjust import based on your email utility function

@receiver(developer_registered)
def send_verification_email_handler(sender, email, token, role, **kwargs):
  try:
    send_verification_email(email, token, role)
    print(f"Verification email sent to {email}.")
  except Exception as e:
    print(f"Failed to send verification email to {email}: {str(e)}")
