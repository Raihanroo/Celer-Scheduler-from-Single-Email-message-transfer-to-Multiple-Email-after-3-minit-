"""
Celery tasks for email sending operations.

Provides background task for sending scheduled emails with
retry logic and comprehensive logging.
"""
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def send_scheduled_emails(self, subject, message, recipient_list):
    """
    Send emails to multiple recipients as a background task.
    
    This task is executed by Celery at scheduled intervals and includes:
    - Individual email sending to each recipient
    - Success/failure tracking
    - Error logging and retry logic
    - Database logging of all operations
    
    Args:
        subject (str): Email subject line
        message (str): Email body content
        recipient_list (list): List of recipient email addresses
        
    Returns:
        dict: Status information including sent/failed counts
        
    Raises:
        Exception: Retries up to 3 times on failure
    """
    from .models import EmailLog
    
    # Create email log entry for tracking
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

        # Send email to each recipient individually
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

        # Update email log with results
        email_log.sent_count = sent_count
        email_log.failed_count = failed_count
        email_log.status = 'sent' if sent_count > 0 else 'failed'
        if errors:
            email_log.error_message = '\n'.join(errors)
        email_log.save()

        return {
            "status": "success",
            "message": f"Email sent to {sent_count} recipient(s)",
            "sent": sent_count,
            "failed": failed_count,
            "recipients": recipient_list,
        }

    except Exception as exc:
        email_log.status = 'failed'
        email_log.error_message = str(exc)
        email_log.save()
        logger.error(f"❌ Error sending email: {exc}")
        # Retry after 60 seconds
        raise self.retry(exc=exc, countdown=60)
