from django.contrib import admin
from .models import EmailLog, ScheduledEmail


@admin.register(EmailLog)
class EmailLogAdmin(admin.ModelAdmin):
    list_display = ['subject', 'status', 'sent_count', 'failed_count', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['subject', 'recipients']
    readonly_fields = ['created_at', 'updated_at']
    
    def has_add_permission(self, request):
        return False  # Admin থেকে manually add করা যাবে না


@admin.register(ScheduledEmail)
class ScheduledEmailAdmin(admin.ModelAdmin):
    list_display = ['task_name', 'subject', 'interval_minutes', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['task_name', 'subject', 'recipients']
    readonly_fields = ['created_at']
