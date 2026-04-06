from django.urls import path
from . import views

urlpatterns = [
    path("", views.EmailFormView.as_view(), name="email-form"),
    path("schedule-email/", views.ScheduleEmailView.as_view(), name="schedule-email"),
    path("send-email/", views.SendImmediateEmailView.as_view(), name="send-email"),
    path("email-history/", views.EmailHistoryView.as_view(), name="email-history"),
    path("scheduled-emails/", views.ScheduledEmailListView.as_view(), name="scheduled-emails"),
]
