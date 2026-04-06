from django.db import models


class EmailLog(models.Model):
    """Email পাঠানোর history track করার জন্য"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('sent', 'Sent'),
        ('failed', 'Failed'),
    ]
    
    subject = models.CharField(max_length=255)
    message = models.TextField()
    recipients = models.JSONField(default=list)  # Multiple emails store করবে
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    sent_count = models.IntegerField(default=0)
    failed_count = models.IntegerField(default=0)
    error_message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Email Log'
        verbose_name_plural = 'Email Logs'
    
    def __str__(self):
        return f"{self.subject} - {self.status}"


class ScheduledEmail(models.Model):
    """Scheduled email configuration"""
    
    task_name = models.CharField(max_length=255, unique=True)
    recipients = models.JSONField(default=list)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    interval_minutes = models.IntegerField(default=3)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.task_name} - {self.recipients}"
