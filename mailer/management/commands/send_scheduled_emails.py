"""
Django Management Command - Automatic Email Sender
এই command চালালে automatically scheduled emails পাঠাবে
"""

from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
from mailer.models import ScheduledEmail, EmailLog
import time
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Send scheduled emails automatically at specified intervals'

    def add_arguments(self, parser):
        parser.add_argument(
            '--interval',
            type=int,
            default=60,
            help='Interval in seconds between email batches (default: 60)'
        )
        parser.add_argument(
            '--once',
            action='store_true',
            help='Send emails once and exit (no loop)'
        )

    def handle(self, *args, **options):
        interval = options['interval']
        run_once = options['once']
        
        self.stdout.write(self.style.SUCCESS('🚀 Email Scheduler Started!'))
        self.stdout.write(f'📧 Interval: {interval} seconds')
        self.stdout.write(f'🔄 Mode: {"Single run" if run_once else "Continuous"}')
        self.stdout.write('-' * 60)
        
        try:
            while True:
                self.send_all_scheduled_emails()
                
                if run_once:
                    self.stdout.write(self.style.SUCCESS('✅ Single run completed!'))
                    break
                
                self.stdout.write(f'⏳ Waiting {interval} seconds...\n')
                time.sleep(interval)
                
        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING('\n⚠️  Scheduler stopped by user'))

    def send_all_scheduled_emails(self):
        """Send emails for all active scheduled email tasks"""
        
        active_schedules = ScheduledEmail.objects.filter(is_active=True)
        
        if not active_schedules.exists():
            self.stdout.write(self.style.WARNING('⚠️  No active scheduled emails found'))
            return
        
        self.stdout.write(f'📬 Found {active_schedules.count()} active schedule(s)')
        
        for schedule in active_schedules:
            self.send_email_batch(schedule)

    def send_email_batch(self, schedule):
        """Send emails for a specific schedule"""
        
        self.stdout.write(f'\n📧 Processing: {schedule.task_name}')
        self.stdout.write(f'   Recipients: {len(schedule.recipients)}')
        self.stdout.write(f'   Subject: {schedule.subject}')
        
        # Create email log
        email_log = EmailLog.objects.create(
            subject=schedule.subject,
            message=schedule.message,
            recipients=schedule.recipients,
            status='pending'
        )
        
        sent_count = 0
        failed_count = 0
        errors = []
        
        for recipient in schedule.recipients:
            try:
                send_mail(
                    subject=schedule.subject,
                    message=schedule.message,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[recipient],
                    fail_silently=False,
                )
                sent_count += 1
                self.stdout.write(self.style.SUCCESS(f'   ✅ Sent to {recipient}'))
                
            except Exception as e:
                failed_count += 1
                error_msg = f'{recipient}: {str(e)}'
                errors.append(error_msg)
                self.stdout.write(self.style.ERROR(f'   ❌ Failed: {error_msg}'))
        
        # Update email log
        email_log.sent_count = sent_count
        email_log.failed_count = failed_count
        email_log.status = 'sent' if sent_count > 0 else 'failed'
        if errors:
            email_log.error_message = '\n'.join(errors)
        email_log.save()
        
        self.stdout.write(self.style.SUCCESS(
            f'   📊 Summary: {sent_count} sent, {failed_count} failed'
        ))
