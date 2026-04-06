# 📧 Multiple Email Configuration Guide

## কোথায় Multiple Emails দিবেন?

এই guide এ বিস্তারিত বলা হয়েছে কিভাবে এবং কোথায় multiple emails configure করবেন।

---

## 🎯 Method 1: Web UI থেকে (সবচেয়ে সহজ)

### Step-by-Step:

1. Browser এ যান: **http://localhost:8000/**

2. **Email Addresses** field এ:
   - প্রথম email টাইপ করুন (যেমন: `user1@example.com`)
   - **Enter** চাপুন
   - Email টি নিচে tag হিসেবে দেখাবে
   - আরো email যোগ করতে চাইলে আবার টাইপ করে Enter চাপুন
   - যতগুলো চান ততগুলো email যোগ করতে পারবেন

3. **Subject** এবং **Message** লিখুন

4. **Interval** সেট করুন (কত মিনিট পর পর mail যাবে)

5. Button click করুন:
   - **Schedule Email** - নির্দিষ্ট interval এ automatic mail
   - **Send Now** - এখনই সব emails এ mail পাঠান

### Example Screenshot Flow:

```
┌─────────────────────────────────────────┐
│ Email Addresses                         │
│ ┌─────────────────────────────────────┐ │
│ │ user1@example.com [Enter]           │ │
│ └─────────────────────────────────────┘ │
│                                         │
│ Added Emails:                           │
│ ┌─────────────────────────────────────┐ │
│ │ [user1@example.com] [×]             │ │
│ │ [user2@example.com] [×]             │ │
│ │ [user3@example.com] [×]             │ │
│ └─────────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

---

## 🔧 Method 2: API Request Body তে

### Postman / Thunder Client / Insomnia:

```http
POST http://localhost:8000/api/schedule-email/
Content-Type: application/json

{
  "emails": [
    "user1@example.com",
    "user2@example.com",
    "user3@example.com",
    "user4@example.com",
    "user5@example.com"
  ],
  "subject": "Your Email Subject",
  "message": "Your email message here",
  "interval_minutes": 3
}
```

### cURL Command:

```bash
curl -X POST http://localhost:8000/api/schedule-email/ \
  -H "Content-Type: application/json" \
  -d '{
    "emails": [
      "user1@example.com",
      "user2@example.com",
      "user3@example.com"
    ],
    "subject": "Test Email",
    "message": "This is a test message",
    "interval_minutes": 3
  }'
```

### Python Requests:

```python
import requests

url = "http://localhost:8000/api/schedule-email/"
data = {
    "emails": [
        "user1@example.com",
        "user2@example.com",
        "user3@example.com",
        "user4@example.com"
    ],
    "subject": "Test Email",
    "message": "This is a test message",
    "interval_minutes": 3
}

response = requests.post(url, json=data)
print(response.json())
```

### JavaScript Fetch:

```javascript
fetch('http://localhost:8000/api/schedule-email/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    emails: [
      'user1@example.com',
      'user2@example.com',
      'user3@example.com'
    ],
    subject: 'Test Email',
    message: 'This is a test message',
    interval_minutes: 3
  })
})
.then(response => response.json())
.then(data => console.log(data));
```

---

## 📝 Method 3: Code এ Directly

### Django View থেকে:

```python
from mailer.tasks import send_scheduled_emails

# Multiple emails define করুন
recipient_list = [
    "user1@example.com",
    "user2@example.com",
    "user3@example.com",
    "user4@example.com"
]

# Task trigger করুন
send_scheduled_emails.delay(
    subject="Your Subject",
    message="Your Message",
    recipient_list=recipient_list
)
```

### Celery Task থেকে:

```python
from celery import shared_task
from mailer.tasks import send_scheduled_emails

@shared_task
def my_custom_task():
    emails = [
        "user1@example.com",
        "user2@example.com",
        "user3@example.com"
    ]
    
    send_scheduled_emails.delay(
        subject="Custom Task Email",
        message="This is from custom task",
        recipient_list=emails
    )
```

---

## 🎨 Method 4: Admin Panel থেকে

1. **http://localhost:8000/admin/** এ যান
2. **Periodic tasks** এ click করুন
3. **Add periodic task** button এ click করুন
4. **Task** select করুন: `mailer.tasks.send_scheduled_emails`
5. **Arguments** field এ JSON format এ দিন:

```json
[
  "Your Subject",
  "Your Message",
  [
    "user1@example.com",
    "user2@example.com",
    "user3@example.com"
  ]
]
```

6. **Interval** select করুন
7. **Save** করুন

---

## 📊 Email List Format

### ✅ Correct Format:

```json
{
  "emails": [
    "user1@example.com",
    "user2@example.com",
    "user3@example.com"
  ]
}
```

### ❌ Wrong Formats:

```json
// Wrong - String instead of array
{
  "emails": "user1@example.com, user2@example.com"
}

// Wrong - Not an array
{
  "emails": "user1@example.com"
}

// Wrong - Invalid email format
{
  "emails": ["user1", "user2@", "@example.com"]
}
```

---

## 🔍 কিভাবে বুঝবেন Multiple Emails এ Mail গেছে?

### Method 1: Admin Panel

1. **http://localhost:8000/admin/** এ যান
2. **Email Logs** এ click করুন
3. Latest entry তে দেখবেন:
   - **Recipients**: সব email addresses
   - **Sent Count**: কতজনকে successfully mail গেছে
   - **Failed Count**: কতজনকে fail হয়েছে
   - **Status**: sent/failed/pending

### Method 2: API থেকে

```bash
GET http://localhost:8000/api/email-history/
```

Response:

```json
{
  "total": 5,
  "logs": [
    {
      "id": 1,
      "subject": "Test Email",
      "recipients": [
        "user1@example.com",
        "user2@example.com",
        "user3@example.com"
      ],
      "status": "sent",
      "sent_count": 3,
      "failed_count": 0,
      "created_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

### Method 3: Celery Worker Logs

Terminal এ Celery worker এর output দেখুন:

```
[2024-01-15 10:30:00] INFO: ✅ Email sent to user1@example.com
[2024-01-15 10:30:01] INFO: ✅ Email sent to user2@example.com
[2024-01-15 10:30:02] INFO: ✅ Email sent to user3@example.com
```

### Method 4: আপনার Email Inbox

প্রতিটি recipient এর inbox এ mail পৌঁছাবে। Email এর header এ দেখবেন:

```
From: your-email@gmail.com
To: user1@example.com
Subject: Your Subject
```

---

## 💡 Best Practices

### 1. Email List Size

- **Small lists** (1-10 emails): Immediate send করতে পারেন
- **Medium lists** (10-100 emails): Scheduled task ভালো
- **Large lists** (100+ emails): Batch processing করুন

### 2. Testing

প্রথমে নিজের email দিয়ে test করুন:

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

### 3. Error Handling

Email list এ invalid email থাকলে:
- Valid emails এ mail যাবে
- Invalid emails skip হবে
- Error log এ details পাবেন

### 4. Rate Limiting

Gmail এর daily limit:
- Free account: 500 emails/day
- Google Workspace: 2000 emails/day

---

## 🎯 Quick Reference

| Method | Location | Format |
|--------|----------|--------|
| Web UI | http://localhost:8000/ | Type & Enter |
| API | `/api/schedule-email/` | JSON array |
| Code | `tasks.py` | Python list |
| Admin | `/admin/` | JSON in Arguments |

---

## 📞 Common Questions

### Q: কতগুলো email একসাথে পাঠাতে পারব?

A: Technical limit নেই, তবে Gmail এর daily limit আছে (500-2000)।

### Q: Email পাঠাতে কত সময় লাগে?

A: প্রতি email এ ~1-2 seconds। 10 emails = ~10-20 seconds।

### Q: Failed emails কি retry হবে?

A: হ্যাঁ, Celery automatically 3 বার retry করবে।

### Q: Duplicate emails পাঠানো যাবে?

A: হ্যাঁ, তবে Web UI তে duplicate prevent করা আছে।

---

## 🚀 Next Steps

1. `.env` file এ আপনার Gmail credentials দিন
2. Server চালু করুন (`start_servers.bat`)
3. Web UI তে গিয়ে test করুন
4. Admin panel এ logs check করুন

Happy Emailing! 📧
