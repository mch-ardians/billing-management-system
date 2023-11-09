from django.core.mail import EmailMessage
from .models import Setting

def email_scheduler_job():
    values = Setting.objects.filter(status='True')
    
    for value in values:
        email = EmailMessage(
                        subject="Daily Reminder for Your Invoice",
                        body=value.text,
                        from_email="mch.ardians.dev@gmail.com",
                        to=[value.email],
                    )
        email.send()