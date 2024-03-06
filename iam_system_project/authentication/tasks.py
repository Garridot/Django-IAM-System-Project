#tasks.py
from celery import shared_task
from iam_system_project import settings
from django.core.mail import EmailMessage
from django.utils.translation import gettext as _

@shared_task(bind=True)
def send_async_email(self,subject, message, recipient_list):
    
    try:
        email = EmailMessage(subject, message, to=recipient_list, from_email=settings.EMAIL_HOST_USER )
        email.send()
        return True
    except Exception as e:
        # Log the exception or print it for debugging
        print(f"Error sending email: {e}")
        return False
