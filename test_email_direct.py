"""
Direct email test - Celery ছাড়াই email পাঠানো
"""

import os
import django

# Django setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings

print("=" * 60)
print("Direct Email Test")
print("=" * 60)

# Email configuration check
print(f"\n📧 Email Configuration:")
print(f"   From: {settings.EMAIL_HOST_USER}")
print(f"   Host: {settings.EMAIL_HOST}")
print(f"   Port: {settings.EMAIL_PORT}")
print(f"   TLS: {settings.EMAIL_USE_TLS}")

# Test email addresses
test_emails = [
    "ashabroo9@gmail.com",
    "marufiqbal5g@gmail.com",
    "kabirraihan249@gmail.com"
]

print(f"\n📬 Sending test email to {len(test_emails)} recipients...")

try:
    for email in test_emails:
        print(f"\n   Sending to: {email}...", end=" ")
        
        send_mail(
            subject="Test Email from Django",
            message="এটি একটি test email। যদি এই mail পান তাহলে বুঝবেন system কাজ করছে।",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False,
        )
        
        print("✅ Sent!")
    
    print("\n" + "=" * 60)
    print("✅ All emails sent successfully!")
    print("📱 Check your mobile inbox now.")
    print("=" * 60)
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\nPossible reasons:")
    print("1. Gmail App Password incorrect")
    print("2. 2-Step Verification not enabled")
    print("3. Network connection issue")
    print("4. Gmail blocking the login")
