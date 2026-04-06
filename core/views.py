from rest_framework.views import APIView
from rest_framework.response import Response


class HomeView(APIView):
    """
    API endpoints এর list দেখানোর জন্য home page
    """
    
    def get(self, request):
        return Response({
            "message": "Welcome to Celery Email Scheduler API",
            "endpoints": {
                "schedule_email": "/api/schedule-email/ [POST]",
                "send_immediate_email": "/api/send-email/ [POST]",
                "email_history": "/api/email-history/ [GET]",
                "scheduled_emails": "/api/scheduled-emails/ [GET]",
                "admin_panel": "/admin/",
            },
            "usage": {
                "schedule_email": {
                    "method": "POST",
                    "body": {
                        "emails": ["email1@example.com", "email2@example.com"],
                        "subject": "Your subject",
                        "message": "Your message",
                        "interval_minutes": 3
                    }
                },
                "send_immediate_email": {
                    "method": "POST",
                    "body": {
                        "emails": ["email1@example.com", "email2@example.com"],
                        "subject": "Your subject",
                        "message": "Your message"
                    }
                }
            }
        })
