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
    HTML UI দিয়ে email পাঠানোর form
    """
    template_name = 'mailer/email_form.html'


class ScheduleEmailView(APIView):
    """
    Multiple emails এ scheduled mail পাঠানোর জন্য API
    """
    
    def post(self, request):
        # User থেকে data নেওয়া
        recipient_list = request.data.get("emails", [])
        subject = request.data.get("subject", "Scheduled Task Mail")
        message = request.data.get("message", "Ei mail-ti proti 3 minute por por jabe.")
        interval_minutes = request.data.get("interval_minutes", 3)

        # Validation
        if not recipient_list or not isinstance(recipient_list, list):
            return Response(
                {"error": "Email list প্রয়োজন (array format এ)"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not subject or not message:
            return Response(
                {"error": "Subject এবং message প্রয়োজন"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Interval schedule তৈরি
            schedule, created = IntervalSchedule.objects.get_or_create(
                every=interval_minutes,
                period=IntervalSchedule.MINUTES,
            )

            # Unique task name তৈরি
            task_name = f"Email_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

            # Scheduled email database এ save করি
            scheduled_email = ScheduledEmail.objects.create(
                task_name=task_name,
                recipients=recipient_list,
                subject=subject,
                message=message,
                interval_minutes=interval_minutes,
            )

            # Periodic task তৈরি
            PeriodicTask.objects.create(
                interval=schedule,
                name=task_name,
                task="mailer.tasks.send_scheduled_emails",
                args=json.dumps([subject, message, recipient_list]),
            )

            return Response({
                "status": "success",
                "message": f"Email scheduler চালু হয়েছে! প্রতি {interval_minutes} মিনিট পর mail যাবে।",
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
    Email পাঠানোর history দেখার জন্য API
    """
    
    def get(self, request):
        logs = EmailLog.objects.all()[:50]  # শেষ 50টি log
        
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
    Scheduled emails এর list দেখার জন্য
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
    তৎক্ষণাৎ multiple emails এ mail পাঠানোর জন্য (without scheduling)
    """
    
    def post(self, request):
        from django.core.mail import send_mail
        from django.conf import settings
        
        recipient_list = request.data.get("emails", [])
        subject = request.data.get("subject", "Immediate Email")
        message = request.data.get("message", "")

        if not recipient_list or not isinstance(recipient_list, list):
            return Response(
                {"error": "Email list প্রয়োজন (array format এ)"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Direct email পাঠাই (Celery ছাড়া)
        sent_count = 0
        failed_count = 0
        errors = []
        
        # Email log তৈরি করি
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
            
            # Log update করি
            email_log.sent_count = sent_count
            email_log.failed_count = failed_count
            email_log.status = 'sent' if sent_count > 0 else 'failed'
            if errors:
                email_log.error_message = '\n'.join(errors)
            email_log.save()
            
            return Response({
                "status": "success",
                "message": f"✅ {sent_count} টি email পাঠানো হয়েছে!",
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
