# 🚀 Quick Start Guide

## 5-Minute Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Email
Edit `.env` file:
```env
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-16-digit-app-password
```

### 3. Setup Database
```bash
python manage.py migrate
```

### 4. Test Email Configuration
```bash
python check_email_status.py
```

### 5. Start Server
```bash
python manage.py runserver
```

Visit: http://localhost:8000/

---

## Send Emails

### Option 1: Send Now (Immediate)
1. Open http://localhost:8000/
2. Add email addresses (press Enter after each)
3. Fill subject and message
4. Click **"Send Now"**
5. Done! ✅

### Option 2: Schedule Emails (Automatic)
1. Open http://localhost:8000/
2. Add email addresses
3. Fill subject and message
4. Set interval (minutes)
5. Click **"Schedule Email"**
6. Run auto sender:
   ```bash
   start_auto_emails.bat
   ```
   OR
   ```bash
   python manage.py send_scheduled_emails --interval=60
   ```

---

## Common Commands

```bash
# Start Django server
python manage.py runserver

# Start auto email sender (60 seconds interval)
python manage.py send_scheduled_emails --interval=60

# Send scheduled emails once (test)
python manage.py send_scheduled_emails --once

# Check email configuration
python check_email_status.py

# Create admin user
python manage.py createsuperuser

# Access admin panel
http://localhost:8000/admin/
```

---

## Troubleshooting

### Emails not sending?
```bash
python check_email_status.py
```

### Check scheduled emails in database
```bash
python manage.py shell
>>> from mailer.models import ScheduledEmail
>>> ScheduledEmail.objects.filter(is_active=True)
```

### View email logs
```bash
python manage.py shell
>>> from mailer.models import EmailLog
>>> EmailLog.objects.all()[:10]
```

---

## Project Structure

```
celery_schedule/
├── mailer/              # Email app
│   ├── models.py       # EmailLog & ScheduledEmail
│   ├── views.py        # API endpoints
│   ├── tasks.py        # Email sending logic
│   └── templates/      # Web UI
├── core/               # Django settings
├── .env                # Email credentials
├── manage.py           # Django CLI
└── README.md           # Full documentation
```

---

## Need Help?

- Full documentation: See `README.md`
- Email issues: Run `python check_email_status.py`
- Admin panel: http://localhost:8000/admin/

---

**That's it! Start sending emails! 📧**
