"""
Email models for tracking and scheduling email operations.
"""
from django.db import models


class EmailLog(models.Model):
    """
    Tracks the history of all email sending operations.
    
    Stores information about sent/failed emails including recipients,
    status, error messages, and timestamps for monitoring and debugging.
    """
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('sent', 'Sent'),
        ('failed', 'Failed'),
    ]
    
    subject = models.CharField(max_length=255, help_text="Email subject line")
    message = models.TextField(help_text="Email body content")
    recipients = models.JSONField(default=list, help_text="List of recipient email addresses")
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending',
        help_text="Current status of the email"
    )
    sent_count = models.IntegerField(default=0, help_text="Number of successfully sent emails")
    failed_count = models.IntegerField(default=0, help_text="Number of failed email attempts")
    error_message = models.TextField(blank=True, null=True, help_text="Error details if any")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Email Log'
        verbose_name_plural = 'Email Logs'
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.subject} - {self.status}"
    
    @property
    def success_rate(self):
        """Calculate the success rate of email sending."""
        total = self.sent_count + self.failed_count
        if total == 0:
            return 0
        return (self.sent_count / total) * 100


class ScheduledEmail(models.Model):
    """
    Configuration for scheduled recurring emails.
    
    Stores email details and scheduling information for automatic
    email sending at specified intervals.
    """
    
    task_name = models.CharField(
        max_length=255, 
        unique=True,
        help_text="Unique identifier for this scheduled task"
    )
    recipients = models.JSONField(default=list, help_text="List of recipient email addresses")
    subject = models.CharField(max_length=255, help_text="Email subject line")
    message = models.TextField(help_text="Email body content")
    interval_minutes = models.IntegerField(
        default=3,
        help_text="Interval in minutes between email sends"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Whether this scheduled email is currently active"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Scheduled Email'
        verbose_name_plural = 'Scheduled Emails'
        indexes = [
            models.Index(fields=['is_active', '-created_at']),
        ]
    
    def __str__(self):
        status = "Active" if self.is_active else "Inactive"
        return f"{self.subject} ({status}) - {len(self.recipients)} recipients"
    
    @property
    def recipient_count(self):
        """Get the number of recipients."""
        return len(self.recipients) if isinstance(self.recipients, list) else 0
