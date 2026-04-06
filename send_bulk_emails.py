"""
Bulk Email Sender - 100+ emails safely পাঠানোর জন্য
"""

import os
import django
import time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from mailer.tasks import send_scheduled_emails

print("=" * 60)
print("Bulk Email Sender")
print("=" * 60)

# আপনার email list এখানে দিন
email_list = [
    "ashabroo9@gmail.com",
    "marufiqbal5g@gmail.com",
    "kabirraihan249@gmail.com",
    # আরো emails যোগ করুন...
]

print(f"\n📧 Total emails to send: {len(email_list)}")

subject = input("Subject: ")
message = input("Message: ")

batch_size = int(input("Batch size (recommended 20): ") or "20")

print(f"\n📬 Sending in batches of {batch_size}...")

# Batch এ ভাগ করুন
batches = [email_list[i:i+batch_size] for i in range(0, len(email_list), batch_size)]

print(f"   Total batches: {len(batches)}")

for i, batch in enumerate(batches, 1):
    print(f"\n   Batch {i}/{len(batches)}: Sending to {len(batch)} recipients...")
    
    # Celery task trigger করুন
    task = send_scheduled_emails.delay(subject, message, batch)
    
    print(f"   ✅ Task ID: {task.id}")
    
    # Next batch এর আগে delay
    if i < len(batches):
        print(f"   ⏳ Waiting 10 seconds before next batch...")
        time.sleep(10)

print("\n" + "=" * 60)
print("✅ All batches queued!")
print("📊 Check Celery Worker terminal for progress")
print("📱 Emails will arrive in your inbox shortly")
print("=" * 60)
