# 📧 Django Email Scheduler - বাংলা গাইড

## 🎯 এই প্রজেক্ট কি করে?

এই প্রজেক্ট দিয়ে আপনি:
- ✅ একসাথে অনেকগুলো email এ mail পাঠাতে পারবেন
- ✅ নির্দিষ্ট সময় পর পর automatic mail পাঠাতে পারবেন
- ✅ তৎক্ষণাৎ mail পাঠাতে পারবেন
- ✅ কোন email এ mail গেছে/যায়নি তা track করতে পারবেন

---

## 🚀 কিভাবে শুরু করবেন?

### ধাপ ১: Dependencies Install করুন

```bash
pip install -r requirements.txt
```

### ধাপ ২: Gmail App Password তৈরি করুন

1. Google Account এ যান: https://myaccount.google.com/
2. Security → 2-Step Verification চালু করুন
3. Security → App Passwords এ যান
4. "Mail" select করে password generate করুন
5. Password টি copy করুন

### ধাপ ৩: .env File তৈরি করুন

```bash
copy .env.example .env
```

`.env` file খুলে আপনার email এবং password দিন:

```env
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password-here
```

### ধাপ ৪: Database Setup করুন

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### ধাপ ৫: Server চালু করুন

#### সহজ উপায় (Windows):
```bash
start_servers.bat
```

এটি automatically 3টি terminal খুলবে।

#### Manual উপায়:

**Terminal 1 - Django Server:**
```bash
python manage.py runserver
```

**Terminal 2 - Celery Worker:**
```bash
celery -A core worker --loglevel=info --pool=solo
```

**Terminal 3 - Celery Beat:**
```bash
celery -A core beat --loglevel=info
```

---

## 📧 কোথায় Multiple Emails দিবেন?

### পদ্ধতি ১: Web UI (সবচেয়ে সহজ)

1. Browser এ যান: **http://localhost:8000/**

2. Email field এ:
   - Email টাইপ করুন (যেমন: `user1@example.com`)
   - **Enter** চাপুন
   - আরো email যোগ করতে চাইলে আবার টাইপ করে Enter চাপুন

3. Subject এবং Message লিখুন

4. Button click করুন:
   - **Schedule Email** - নির্দিষ্ট সময় পর পর automatic mail
   - **Send Now** - এখনই mail পাঠান

### পদ্ধতি ২: API দিয়ে

Postman বা Thunder Client এ:

```http
POST http://localhost:8000/api/schedule-email/
Content-Type: application/json

{
  "emails": [
    "user1@example.com",
    "user2@example.com",
    "user3@example.com"
  ],
  "subject": "Test Email",
  "message": "এটি একটি test message",
  "interval_minutes": 3
}
```

### পদ্ধতি ৩: Python Script দিয়ে

```bash
python test_api.py
```

---

## 🔍 কিভাবে বুঝবেন Mail গেছে কিনা?

### উপায় ১: Admin Panel

1. যান: **http://localhost:8000/admin/**
2. Login করুন
3. **Email Logs** এ click করুন
4. দেখুন:
   - কতজনকে mail গেছে (Sent Count)
   - কতজনকে fail হয়েছে (Failed Count)
   - কোন error হয়েছে কিনা

### উপায় ২: API থেকে

```bash
GET http://localhost:8000/api/email-history/
```

### উপায় ৩: Celery Worker এর Log

Terminal এ দেখুন:

```
✅ Email sent to user1@example.com
✅ Email sent to user2@example.com
✅ Email sent to user3@example.com
```

### উপায় ৪: Email Inbox

প্রতিটি recipient এর inbox এ mail পৌঁছাবে।

---

## 📊 Available API Endpoints

| URL | Method | কাজ |
|-----|--------|-----|
| `/` | GET | Web UI |
| `/api/schedule-email/` | POST | Schedule email |
| `/api/send-email/` | POST | Immediate email |
| `/api/email-history/` | GET | Email history |
| `/api/scheduled-emails/` | GET | Scheduled emails list |
| `/admin/` | GET | Admin panel |

---

## 🎨 Web UI Features

- ✅ সুন্দর responsive design
- ✅ Email add/remove করা যায়
- ✅ Real-time validation
- ✅ Success/error messages
- ✅ বাংলা language support

---

## 🔧 Troubleshooting

### সমস্যা ১: Email পাঠাতে পারছি না

**সমাধান:**
- Gmail App Password সঠিক আছে কিনা check করুন
- 2-Step Verification চালু আছে কিনা দেখুন
- `.env` file এ credentials সঠিক আছে কিনা check করুন
- Celery worker চালু আছে কিনা check করুন

### সমস্যা ২: Celery Error

**সমাধান:**
Windows এ অবশ্যই `--pool=solo` ব্যবহার করুন:

```bash
celery -A core worker --loglevel=info --pool=solo
```

### সমস্যা ৩: Database Error

**সমাধান:**
```bash
python manage.py flush
python manage.py migrate
```

---

## 📁 Important Files

```
📂 Project Root
├── 📄 .env                      ← আপনার email credentials এখানে
├── 📄 .env.example              ← Example file
├── 📄 requirements.txt          ← Dependencies
├── 📄 manage.py                 ← Django management
├── 📄 start_servers.bat         ← Quick start script
├── 📄 test_api.py               ← API test script
│
├── 📂 core/
│   ├── 📄 settings.py           ← Email configuration এখানে
│   ├── 📄 urls.py               ← URL routing
│   └── 📄 celery.py             ← Celery config
│
├── 📂 mailer/
│   ├── 📄 models.py             ← Database models
│   ├── 📄 views.py              ← API views + Web UI
│   ├── 📄 tasks.py              ← Email sending task
│   ├── 📄 admin.py              ← Admin configuration
│   └── 📂 templates/
│       └── 📂 mailer/
│           └── 📄 email_form.html  ← Web UI
│
└── 📂 Documentation/
    ├── 📄 README.md             ← Main documentation
    ├── 📄 SETUP_GUIDE.md        ← Setup guide
    ├── 📄 MULTIPLE_EMAIL_GUIDE.md  ← Email config guide
    ├── 📄 PROJECT_SUMMARY.md    ← Project summary
    └── 📄 BANGLA_GUIDE.md       ← এই file
```

---

## 💡 Tips & Tricks

### Tip 1: Testing এর জন্য

নিজের email দিয়ে test করুন:

```json
{
  "emails": [
    "your-email@gmail.com",
    "your-email+test1@gmail.com",
    "your-email+test2@gmail.com"
  ]
}
```

Gmail এ `+` দিয়ে multiple aliases তৈরি করতে পারেন।

### Tip 2: Interval Setting

- Development: 1-3 minutes
- Production: 5-60 minutes

### Tip 3: Email Limit

Gmail daily limit:
- Free account: 500 emails/day
- Google Workspace: 2000 emails/day

---

## ✅ Testing Checklist

সব ঠিক আছে কিনা check করুন:

- [ ] Server চালু হচ্ছে
- [ ] Celery worker চালু হচ্ছে
- [ ] Celery beat চালু হচ্ছে
- [ ] Web UI খুলছে (http://localhost:8000/)
- [ ] Email add করা যাচ্ছে
- [ ] Schedule email কাজ করছে
- [ ] Send now কাজ করছে
- [ ] Admin panel খুলছে
- [ ] Email logs দেখা যাচ্ছে
- [ ] Multiple emails এ mail যাচ্ছে

---

## 🎯 Quick Commands

### Setup Commands
```bash
pip install -r requirements.txt
copy .env.example .env
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### Run Commands
```bash
# Quick start (Windows)
start_servers.bat

# Manual
python manage.py runserver
celery -A core worker --loglevel=info --pool=solo
celery -A core beat --loglevel=info
```

### Test Commands
```bash
python test_api.py
```

---

## 📞 সাহায্য প্রয়োজন?

### Debug করার জন্য:

1. **Celery logs দেখুন:**
   ```bash
   celery -A core worker --loglevel=debug
   ```

2. **Django logs দেখুন:**
   Terminal এ server এর output দেখুন

3. **Admin panel check করুন:**
   http://localhost:8000/admin/

4. **Email history check করুন:**
   http://localhost:8000/api/email-history/

---

## 🎉 Success!

আপনার system ঠিকমতো কাজ করছে যদি:

1. ✅ Web UI তে email add করতে পারেন
2. ✅ Button click করলে mail যায়
3. ✅ Admin panel এ logs দেখা যায়
4. ✅ Terminal এ "✅ Email sent" message দেখা যায়
5. ✅ Recipient এর inbox এ mail পৌঁছায়

---

## 📚 আরো জানতে

- **English Documentation:** README.md
- **Setup Guide:** SETUP_GUIDE.md
- **Multiple Email Guide:** MULTIPLE_EMAIL_GUIDE.md
- **Project Summary:** PROJECT_SUMMARY.md

---

**শুভকামনা! 📧**

আপনার email scheduler এখন ready! 🎉
