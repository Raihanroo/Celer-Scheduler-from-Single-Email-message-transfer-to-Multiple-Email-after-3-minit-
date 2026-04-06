# 🚀 Complete Setup Guide - Django Email Scheduler

## ধাপে ধাপে Setup করার নিয়ম

### Step 1: Project Clone/Download করুন

```bash
cd your-project-folder
```

### Step 2: Virtual Environment তৈরি করুন (Optional but Recommended)

```bash
# Virtual environment তৈরি
python -m venv venv

# Activate করুন
# Windows:
venv\Scripts\activate

# Linux/Mac:
source venv/bin/activate
```

### Step 3: Dependencies Install করুন

```bash
pip install -r requirements.txt
```

### Step 4: Environment Variables Setup

1. `.env.example` file কপি করে `.env` তৈরি করুন:

```bash
copy .env.example .env
```

2. `.env` file খুলে আপনার email credentials দিন:

```env
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password-here
```

### Step 5: Gmail App Password তৈরি করুন

1. আপনার Google Account এ যান: https://myaccount.google.com/
2. Security → 2-Step Verification চালু করুন
3. Security → App Passwords এ যান
4. "Select app" → "Mail" select করুন
5. "Select device" → "Other" select করে "Django App" লিখুন
6. Generate করুন
7. Generated 16-digit password টি copy করে `.env` file এ `EMAIL_HOST_PASSWORD` এ দিন

### Step 6: Database Setup

```bash
# Migrations তৈরি করুন
python manage.py makemigrations

# Database migrate করুন
python manage.py migrate

# Admin user তৈরি করুন
python manage.py createsuperuser
```

### Step 7: Server চালু করুন

আপনাকে 3টি terminal window খুলতে হবে:

#### Terminal 1 - Django Server

```bash
python manage.py runserver
```

#### Terminal 2 - Celery Worker

```bash
# Windows:
celery -A core worker --loglevel=info --pool=solo

# Linux/Mac:
celery -A core worker --loglevel=info
```

#### Terminal 3 - Celery Beat (Scheduled tasks এর জন্য)

```bash
celery -A core beat --loglevel=info
```

## 📧 কিভাবে Multiple Emails পাঠাবেন?

### Method 1: Web UI ব্যবহার করে (সবচেয়ে সহজ)

1. Browser এ যান: http://localhost:8000/
2. Email addresses টাইপ করে Enter চাপুন (যতগুলো চান)
3. Subject এবং Message লিখুন
4. "Schedule Email" অথবা "Send Now" button এ click করুন

### Method 2: API ব্যবহার করে

#### Postman/Thunder Client দিয়ে:

```
POST http://localhost:8000/api/schedule-email/
Content-Type: application/json

{
  "emails": [
    "user1@example.com",
    "user2@example.com",
    "user3@example.com",
    "user4@example.com"
  ],
  "subject": "Test Email",
  "message": "এটি একটি test message",
  "interval_minutes": 3
}
```

#### Python Script দিয়ে:

```bash
python test_api.py
```

### Method 3: cURL দিয়ে

```bash
curl -X POST http://localhost:8000/api/schedule-email/ \
  -H "Content-Type: application/json" \
  -d '{
    "emails": ["test1@example.com", "test2@example.com"],
    "subject": "Test Email",
    "message": "Test message",
    "interval_minutes": 3
  }'
```

## 🎯 Multiple Email Configuration এর জায়গা

### 1. API Request Body তে

```json
{
  "emails": [
    "email1@example.com",
    "email2@example.com",
    "email3@example.com"
  ]
}
```

### 2. Web UI তে

- Email input field এ email টাইপ করুন
- Enter চাপুন
- আরো email যোগ করতে চাইলে আবার টাইপ করে Enter চাপুন
- সব emails নিচে tag হিসেবে দেখাবে

## 📊 Email Tracking

### Admin Panel থেকে দেখুন:

1. http://localhost:8000/admin/ এ যান
2. Login করুন (createsuperuser দিয়ে তৈরি করা username/password)
3. "Email Logs" এ click করুন
4. সব email এর history দেখতে পারবেন:
   - কতজনকে successfully mail গেছে
   - কোন email fail হয়েছে কিনা
   - Error messages

### API থেকে দেখুন:

```bash
# Email history
GET http://localhost:8000/api/email-history/

# Scheduled emails list
GET http://localhost:8000/api/scheduled-emails/
```

## 🔧 Troubleshooting

### Email পাঠাতে সমস্যা হলে:

1. Gmail App Password সঠিক আছে কিনা check করুন
2. 2-Step Verification চালু আছে কিনা দেখুন
3. `.env` file এ credentials সঠিক আছে কিনা check করুন
4. Celery worker চালু আছে কিনা check করুন

### Celery Error হলে:

Windows এ Celery চালাতে অবশ্যই `--pool=solo` ব্যবহার করুন:

```bash
celery -A core worker --loglevel=info --pool=solo
```

### Database Error হলে:

```bash
# Database reset করুন
python manage.py flush

# আবার migrate করুন
python manage.py migrate
```

## 📁 Project Structure

```
.
├── core/                      # Main Django project
│   ├── settings.py           # Settings (EMAIL_HOST_USER এখানে)
│   ├── urls.py               # Main URL routing
│   ├── celery.py             # Celery configuration
│   └── views.py              # Home API view
├── mailer/                   # Email app
│   ├── models.py             # EmailLog, ScheduledEmail models
│   ├── views.py              # API views + EmailFormView
│   ├── tasks.py              # Celery tasks (send_scheduled_emails)
│   ├── urls.py               # App URLs
│   ├── admin.py              # Admin configuration
│   └── templates/
│       └── mailer/
│           └── email_form.html  # Web UI
├── .env                      # আপনার credentials (create করতে হবে)
├── .env.example              # Example file
├── requirements.txt          # Dependencies
├── README.md                 # Main documentation
├── SETUP_GUIDE.md           # এই file
└── test_api.py              # API test script
```

## 🎉 সব ঠিক আছে কিনা Test করুন

1. Server চালু করুন (3টি terminal)
2. Browser এ http://localhost:8000/ খুলুন
3. আপনার নিজের email address দিয়ে test করুন
4. Admin panel এ গিয়ে log check করুন

## 💡 Tips

- Development এর সময় interval_minutes কম রাখুন (1-3 minutes)
- Production এ interval বাড়িয়ে দিন
- Email logs regularly check করুন
- Failed emails এর error messages পড়ুন

## 📞 Support

কোন সমস্যা হলে:
1. Error logs check করুন
2. Celery worker এর output দেখুন
3. Admin panel এ email logs check করুন
