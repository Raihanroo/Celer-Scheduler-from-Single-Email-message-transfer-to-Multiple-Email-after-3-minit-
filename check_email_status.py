"""
Email Status Checker - কোথায় সমস্যা হচ্ছে তা খুঁজে বের করুন
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.conf import settings
from django.core.mail import send_mail
import smtplib

print("=" * 70)
print("📧 Email Configuration Checker")
print("=" * 70)

# Step 1: Check settings
print("\n1️⃣ Checking Email Settings...")
print(f"   EMAIL_HOST: {settings.EMAIL_HOST}")
print(f"   EMAIL_PORT: {settings.EMAIL_PORT}")
print(f"   EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
print(f"   EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
print(f"   EMAIL_HOST_PASSWORD: {'*' * len(settings.EMAIL_HOST_PASSWORD) if settings.EMAIL_HOST_PASSWORD else 'NOT SET'}")

if not settings.EMAIL_HOST_USER or settings.EMAIL_HOST_USER == "your-email@gmail.com":
    print("   ❌ EMAIL_HOST_USER not configured properly!")
    print("   Fix: Edit .env file and add your Gmail address")
    exit()

if not settings.EMAIL_HOST_PASSWORD or settings.EMAIL_HOST_PASSWORD == "your-app-password-here":
    print("   ❌ EMAIL_HOST_PASSWORD not configured properly!")
    print("   Fix: Edit .env file and add your Gmail App Password")
    exit()

print("   ✅ Settings look good")

# Step 2: Test SMTP connection
print("\n2️⃣ Testing SMTP Connection...")
try:
    server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
    server.starttls()
    server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
    server.quit()
    print("   ✅ SMTP connection successful")
except smtplib.SMTPAuthenticationError:
    print("   ❌ Authentication failed!")
    print("   Reasons:")
    print("      - Wrong email or password")
    print("      - 2-Step Verification not enabled")
    print("      - App Password not generated")
    print("      - Using regular password instead of App Password")
    exit()
except Exception as e:
    print(f"   ❌ Connection failed: {e}")
    exit()

# Step 3: Send test email
print("\n3️⃣ Sending Test Email...")
test_email = input("   Enter your email to receive test: ")

try:
    send_mail(
        subject="✅ Test Email - Django Email Scheduler",
        message="""
এটি একটি test email।

যদি আপনি এই mail পান তাহলে বুঝবেন:
✅ Email configuration সঠিক
✅ Gmail connection কাজ করছে
✅ System ready

এখন UI থেকে email পাঠাতে পারবেন।

ধন্যবাদ!
        """,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[test_email],
        fail_silently=False,
    )
    print(f"   ✅ Test email sent to {test_email}")
    print("\n" + "=" * 70)
    print("📱 Check Your Email Now!")
    print("=" * 70)
    print("\n🔍 Where to check:")
    print("   1. Inbox (Primary tab)")
    print("   2. Spam/Junk folder")
    print("   3. Promotions tab (Gmail)")
    print("   4. All Mail folder")
    print("\n⏳ Wait 1-2 minutes for email to arrive")
    print("\n💡 If still not received:")
    print("   - Check Spam folder")
    print("   - Search for 'Django Email Scheduler'")
    print("   - Check 'All Mail' in Gmail")
    
except Exception as e:
    print(f"   ❌ Failed to send: {e}")
    print("\n🔧 Troubleshooting:")
    print("   1. Check .env file has correct credentials")
    print("   2. Verify Gmail App Password is correct")
    print("   3. Ensure 2-Step Verification is ON")
    print("   4. Try generating new App Password")
