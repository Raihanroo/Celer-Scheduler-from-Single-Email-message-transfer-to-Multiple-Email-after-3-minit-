"""
100 Email Test - Check if system can handle bulk emails
"""

import os
import django
import time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings

print("=" * 60)
print("100 Email Bulk Test")
print("=" * 60)

# Generate 100 test emails using Gmail alias trick
# your-email+1@gmail.com, your-email+2@gmail.com etc.
base_emails = [
    "ashabroo9@gmail.com",
    "marufiqbal5g@gmail.com",
    "kabirraihan249@gmail.com"
]

# Create 100 emails using aliases
test_emails = []
for i in range(1, 101):
    # Use modulo to cycle through base emails
    base = base_emails[i % len(base_emails)]
    # Add +number before @
    email_parts = base.split('@')
    aliased_email = f"{email_parts[0]}+test{i}@{email_parts[1]}"
    test_emails.append(aliased_email)

print(f"\n📧 Generated {len(test_emails)} test email addresses")
print(f"   Example: {test_emails[0]}, {test_emails[1]}, ...")

choice = input("\n⚠️  Do you want to send 100 test emails? (yes/no): ")

if choice.lower() != 'yes':
    print("❌ Test cancelled.")
    exit()

print(f"\n📬 Sending emails to {len(test_emails)} recipients...")
print("   This will take approximately 2-3 minutes...")

success_count = 0
failed_count = 0
start_time = time.time()

for i, email in enumerate(test_emails, 1):
    try:
        send_mail(
            subject=f"Bulk Test Email #{i}",
            message=f"এটি bulk test email #{i}। Total {len(test_emails)} emails পাঠানো হচ্ছে।",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False,
        )
        success_count += 1
        
        # Progress indicator
        if i % 10 == 0:
            elapsed = time.time() - start_time
            print(f"   ✅ {i}/{len(test_emails)} sent ({elapsed:.1f}s)")
        
        # Small delay to avoid rate limiting
        time.sleep(0.1)
        
    except Exception as e:
        failed_count += 1
        print(f"   ❌ Failed to send to {email}: {e}")

end_time = time.time()
total_time = end_time - start_time

print("\n" + "=" * 60)
print("📊 Results:")
print(f"   ✅ Successfully sent: {success_count}")
print(f"   ❌ Failed: {failed_count}")
print(f"   ⏱️  Total time: {total_time:.2f} seconds")
print(f"   📈 Average: {total_time/len(test_emails):.2f}s per email")
print("=" * 60)

if success_count > 0:
    print("\n✅ System can handle bulk emails!")
    print("📱 Check your inbox (emails will arrive in batches)")
else:
    print("\n❌ All emails failed. Check your Gmail settings.")
