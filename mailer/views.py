"""
API views for email sending and scheduling operations.

Provides endpoints for:
- Displaying email form UI
- Sending immediate emails
- Scheduling recurring emails
- Viewing email history and scheduled tasks
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.generic import TemplateView
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from .models import EmailLog, ScheduledEmail
from .tasks import send_scheduled_emails
import json
from datetime import datetime


class EmailFormView(TemplateView):
    """
    Renders the email form UI for sending emails.
    
    Provides a user-friendly interface with email tag system
    for adding multiple recipients and sending emails.
    """
    template_name = 'mailer/email_form.html'


class ScheduleEmailView(APIView):
    """
    API endpoint for scheduling recurring emails to multiple recipients.
    
    Creates a scheduled task that will send emails at specified intervals
    using the management command or Celery (if configured).
    
    Request body:
        - emails: List of recipient email addresses
        - subject: Email subject line
        - message: Email body content
        - interval_minutes: Time interval between sends (default: 3)
    """
    
    def post(self, request):
        # Extract data from request
        recipient_list = request.data.get("emails", [])
        subject = request.data.get("subject", "Scheduled Task Mail")
        message = request.data.get("message", "This email will be sent at regular intervals.")
        interval_minutes = request.data.get("interval_minutes", 3)

        # Validate input
        if not recipient_list or not isinstance(recipient_list, list):
            return Response(
                {"error": "Email list is required (must be an array)"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not subject or not message:
            return Response(
                {"error": "Subject and message are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Create interval schedule
            schedule, created = IntervalSchedule.objects.get_or_create(
                every=interval_minutes,
                period=IntervalSchedule.MINUTES,
            )

            # Generate unique task name
            task_name = f"Email_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

            # Save scheduled email to database
            scheduled_email = ScheduledEmail.objects.create(
                task_name=task_name,
                recipients=recipient_list,
                subject=subject,
                message=message,
                interval_minutes=interval_minutes,
            )

            # Create periodic task for Celery
            PeriodicTask.objects.create(
                interval=schedule,
                name=task_name,
                task="mailer.tasks.send_scheduled_emails",
                args=json.dumps([subject, message, recipient_list]),
            )

            return Response({
                "status": "success",
                "message": f"Email scheduler activated! Emails will be sent every {interval_minutes} minute(s).",
                "task_name": task_name,
                "recipients": recipient_list,
                "interval_minutes": interval_minutes,
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {"error": f"Error: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class EmailHistoryView(APIView):
    """
    API endpoint for viewing email sending history.
    
    Returns the last 50 email logs with status, recipients,
    and error information if any.
    """
    
    def get(self, request):
        logs = EmailLog.objects.all()[:50]  # Last 50 logs
        
        data = [{
            "id": log.id,
            "subject": log.subject,
            "recipients": log.recipients,
            "status": log.status,
            "sent_count": log.sent_count,
            "failed_count": log.failed_count,
            "error_message": log.error_message,
            "created_at": log.created_at,
        } for log in logs]
        
        return Response({
            "total": logs.count(),
            "logs": data
        })


class ScheduledEmailListView(APIView):
    """
    API endpoint for listing all active scheduled emails.
    
    Returns information about currently active scheduled tasks
    including recipients, subject, and interval settings.
    """
    
    def get(self, request):
        scheduled_emails = ScheduledEmail.objects.filter(is_active=True)
        
        data = [{
            "id": email.id,
            "task_name": email.task_name,
            "recipients": email.recipients,
            "subject": email.subject,
            "interval_minutes": email.interval_minutes,
            "created_at": email.created_at,
        } for email in scheduled_emails]
        
        return Response({
            "total": scheduled_emails.count(),
            "scheduled_emails": data
        })


class SendImmediateEmailView(APIView):
    """
    API endpoint for sending immediate emails to multiple recipients.
    
    Sends emails directly without scheduling, providing instant delivery.
    Tracks success/failure for each recipient and logs the results.
    
    Request body:
        - emails: List of recipient email addresses
        - subject: Email subject line
        - message: Email body content
    """
    
    def post(self, request):
        from django.core.mail import send_mail
        from django.conf import settings
        
        recipient_list = request.data.get("emails", [])
        subject = request.data.get("subject", "Immediate Email")
        message = request.data.get("message", "")

        if not recipient_list or not isinstance(recipient_list, list):
            return Response(
                {"error": "Email list is required (must be an array)"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Send emails directly (without Celery)
        sent_count = 0
        failed_count = 0
        errors = []
        
        # Create email log entry
        email_log = EmailLog.objects.create(
            subject=subject,
            message=message,
            recipients=recipient_list,
            status='pending'
        )
        
        try:
            for recipient in recipient_list:
                try:
                    send_mail(
                        subject=subject,
                        message=message,
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[recipient],
                        fail_silently=False,
                    )
                    sent_count += 1
                except Exception as e:
                    failed_count += 1
                    errors.append(f"{recipient}: {str(e)}")
            
            # Update email log
            email_log.sent_count = sent_count
            email_log.failed_count = failed_count
            email_log.status = 'sent' if sent_count > 0 else 'failed'
            if errors:
                email_log.error_message = '\n'.join(errors)
            email_log.save()
            
            return Response({
                "status": "success",
                "message": f"✅ {sent_count} email(s) sent successfully!",
                "sent_count": sent_count,
                "failed_count": failed_count,
                "recipients": recipient_list,
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            email_log.status = 'failed'
            email_log.error_message = str(e)
            email_log.save()
            
            return Response(
                {"error": f"Error: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
