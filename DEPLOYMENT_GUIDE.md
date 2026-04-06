# 🚀 Deployment Guide - Django Email Scheduler

## Railway.app এ Deploy করার নিয়ম (Recommended)

### ধাপ ১: Railway Account তৈরি করুন

1. যান: https://railway.app/
2. "Start a New Project" click করুন
3. GitHub দিয়ে login করুন

### ধাপ ২: Project Setup

1. "Deploy from GitHub repo" select করুন
2. আপনার repository select করুন:
   `Celer-Scheduler-from-Single-Email-message-transfer-to-Multiple-Email-after-3-minit-`
3. "Deploy Now" click করুন

### ধাপ ৩: Environment Variables Add করুন

Railway dashboard এ যান এবং Variables tab এ:

```env
SECRET_KEY=your-secret-key-here-generate-new-one
DEBUG=False
ALLOWED_HOSTS=*.railway.app
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DATABASE_URL=postgresql://... (Railway automatically provide করবে)
CELERY_BROKER_URL=redis://... (Railway Redis add করলে)
```

### ধাপ ৪: Redis Add করুন

1. Railway dashboard এ "New" click করুন
2. "Database" → "Redis" select করুন
3. Automatically `REDIS_URL` environment variable add হবে

### ধাপ ৫: PostgreSQL Add করুন (Optional)

1. "New" → "Database" → "PostgreSQL"
2. Automatically `DATABASE_URL` add হবে

### ধাপ ৬: Deploy!

Railway automatically deploy করবে। URL পাবেন:
```
https://your-app-name.railway.app
```

---

## Render.com এ Deploy (Free Tier)

### ধাপ ১: Render Account

1. যান: https://render.com/
2. GitHub দিয়ে signup করুন

### ধাপ ২: New Web Service

1. "New" → "Web Service"
2. GitHub repository connect করুন
3. Settings:
   - **Name**: django-email-scheduler
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn core.wsgi:application`

### ধাপ ৩: Environment Variables

```env
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=.onrender.com
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
PYTHON_VERSION=3.11.0
```

### ধাপ ৪: Redis Add করুন

1. "New" → "Redis"
2. Copy Redis URL
3. Web Service এ `CELERY_BROKER_URL` add করুন

---

## PythonAnywhere (Free Tier - সহজ)

### ধাপ ১: Account তৈরি

1. যান: https://www.pythonanywhere.com/
2. Free account তৈরি করুন

### ধাপ ২: Code Upload

Bash console এ:

```bash
git clone https://github.com/Raihanroo/Celer-Scheduler-from-Single-Email-message-transfer-to-Multiple-Email-after-3-minit-.git
cd Celer-Scheduler-from-Single-Email-message-transfer-to-Multiple-Email-after-3-minit-
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic
```

### ধাপ ৩: Web App Setup

1. "Web" tab এ যান
2. "Add a new web app"
3. "Manual configuration" → Python 3.11
4. WSGI file edit করুন:

```python
import os
import sys

path = '/home/yourusername/Celer-Scheduler-from-Single-Email-message-transfer-to-Multiple-Email-after-3-minit-'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### ধাপ ৪: Environment Variables

Files tab → `.env` file তৈরি করুন

---

## ⚠️ Important Notes

### 1. Secret Key Generate করুন

```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 2. ALLOWED_HOSTS Update করুন

Production এ:
```python
ALLOWED_HOSTS = [
    'your-app.railway.app',
    'your-app.onrender.com',
    'yourusername.pythonanywhere.com'
]
```

### 3. DEBUG = False

Production এ অবশ্যই `DEBUG=False` রাখুন

### 4. Static Files

```bash
python manage.py collectstatic
```

### 5. Database Migration

```bash
python manage.py migrate
```

---

## 🎯 Comparison

| Platform | Free Tier | Celery Support | Ease | Best For |
|----------|-----------|----------------|------|----------|
| Railway | 500 hrs/month | ✅ Yes | ⭐⭐⭐⭐⭐ | Production |
| Render | Yes | ✅ Yes | ⭐⭐⭐⭐ | Production |
| PythonAnywhere | Yes | ❌ Limited | ⭐⭐⭐ | Simple apps |
| Heroku | No (Paid) | ✅ Yes | ⭐⭐⭐⭐ | Enterprise |

---

## 🚀 Recommended: Railway.app

**কেন Railway?**
- ✅ সবচেয়ে সহজ setup
- ✅ Automatic deployments
- ✅ Redis/PostgreSQL built-in
- ✅ Celery worker support
- ✅ Free tier generous

---

## 📝 Deployment Checklist

- [ ] GitHub repository updated
- [ ] Environment variables configured
- [ ] Secret key generated
- [ ] DEBUG=False
- [ ] ALLOWED_HOSTS updated
- [ ] Static files collected
- [ ] Database migrated
- [ ] Redis configured (for Celery)
- [ ] Email credentials added
- [ ] Test deployment

---

## 🔗 Useful Links

- Railway: https://railway.app/
- Render: https://render.com/
- PythonAnywhere: https://www.pythonanywhere.com/
- Django Deployment: https://docs.djangoproject.com/en/5.2/howto/deployment/

---

**Deploy করার পর test করুন:**
1. URL খুলুন
2. Email form দেখা যাচ্ছে কিনা
3. Email পাঠান
4. Mobile এ mail check করুন

Good luck! 🎉
