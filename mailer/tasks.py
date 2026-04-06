from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def send_scheduled_emails(self, subject, message, recipient_list):
    """
    প্রতি 3 মিনিট অন্তর multiple emails এ mail পাঠায়
    Dashboard এ track করা যায়
    """
    from .models import EmailLog
    
    # Email log entry তৈরি করি
    email_log = EmailLog.objects.create(
        subject=subject,
        message=message,
        recipients=recipient_list,
        status='pending'
    )
    
    sent_count = 0
    failed_count = 0
    errors = []
    
    try:
        email_from = settings.EMAIL_HOST_USER

        # প্রতিটি email এ আলাদা mail পাঠাই
        for recipient in recipient_list:
            try:
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=email_from,
                    recipient_list=[recipient],
                    fail_silently=False,
                )
                sent_count += 1
                logger.info(f"✅ Email sent to {recipient}")
            except Exception as e:
                failed_count += 1
                error_msg = f"Failed to send to {recipient}: {str(e)}"
                errors.append(error_msg)
                logger.error(f"❌ {error_msg}")

        # Email log update করি
        email_log.sent_count = sent_count
        email_log.failed_count = failed_count
        email_log.status = 'sent' if sent_count > 0 else 'failed'
        if errors:
            email_log.error_message = '\n'.join(errors)
        email_log.save()

        return {
            "status": "success",
            "message": f"Mail {sent_count} জন এর কাছে পাঠানো হয়েছে",
            "sent": sent_count,
            "failed": failed_count,
            "recipients": recipient_list,
        }

    except Exception as exc:
        email_log.status = 'failed'
        email_log.error_message = str(exc)
        email_log.save()
        logger.error(f"❌ Error sending email: {exc}")
        raise self.retry(exc=exc, countdown=60)
