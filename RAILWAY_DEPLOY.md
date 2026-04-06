# 🚀 Railway.app এ Deploy - Step by Step

## ধাপ ১: Railway Account তৈরি করুন

1. যান: **https://railway.app/**
2. **"Start a New Project"** click করুন
3. **GitHub দিয়ে login** করুন (GitHub account লাগবে)

## ধাপ ২: GitHub Repository Connect করুন

1. **"Deploy from GitHub repo"** select করুন
2. আপনার repository খুঁজুন:
   ```
   Celer-Scheduler-from-Single-Email-message-transfer-to-Multiple-Email-after-3-minit-
   ```
3. Repository select করুন
4. **"Deploy Now"** click করুন

## ধাপ ৩: Environment Variables Add করুন

Railway dashboard এ **"Variables"** tab এ যান এবং add করুন:

```env
SECRET_KEY=django-insecure-CHANGE-THIS-TO-RANDOM-STRING
DEBUG=False
ALLOWED_HOSTS=*.railway.app
EMAIL_HOST_USER=raihanroo21@gmail.com
EMAIL_HOST_PASSWORD=bcvklomzstrcxzzc
CELERY_BROKER_URL=${{Redis.REDIS_URL}}
CELERY_RESULT_BACKEND=${{Redis.REDIS_URL}}
```

### Secret Key Generate করুন:

Terminal এ run করুন:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy করে `SECRET_KEY` এ paste করুন।

## ধাপ ৪: Redis Add করুন (Celery এর জন্য)

1. Railway dashboard এ **"New"** button click করুন
2. **"Database"** → **"Add Redis"** select করুন
3. Redis automatically connect হবে
4. `REDIS_URL` environment variable automatically add হবে

## ধাপ ৫: PostgreSQL Add করুন (Optional - Better than SQLite)

1. **"New"** → **"Database"** → **"Add PostgreSQL"**
2. Automatically `DATABASE_URL` add হবে
3. Django automatically PostgreSQL use করবে

## ধাপ ৬: Deploy Settings Check করুন

Railway automatically detect করবে:

- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python manage.py migrate && gunicorn core.wsgi:application`

যদি manually set করতে হয়:

1. **Settings** tab এ যান
2. **Deploy** section এ:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python manage.py migrate && gunicorn core.wsgi:application`

## ধাপ ৭: Celery Worker Add করুন (Optional)

Scheduled emails এর জন্য:

1. **"New"** → **"Empty Service"**
2. Same GitHub repo select করুন
3. **Start Command**: `celery -A core worker --loglevel=info`
4. Same environment variables add করুন

## ধাপ ৮: Celery Beat Add করুন (Optional)

1. **"New"** → **"Empty Service"**
2. Same GitHub repo select করুন
3. **Start Command**: `celery -A core beat --loglevel=info`
4. Same environment variables add করুন

## ধাপ ৯: Deploy Complete!

Railway automatically deploy করবে। কয়েক মিনিট পর:

1. **"Deployments"** tab এ যান
2. **"View Logs"** click করে check করুন
3. **Domain** পাবেন:
   ```
   https://your-app-name.railway.app
   ```

## ধাপ ১০: Test করুন

1. Browser এ আপনার Railway URL খুলুন
2. Email form দেখা যাচ্ছে কিনা check করুন
3. Test email পাঠান
4. Mobile এ mail check করুন

---

## 🔧 Troubleshooting

### Error: "Application failed to respond"

**Solution:**
```env
PORT=8000
```
Environment variables এ add করুন।

### Error: "Static files not found"

**Solution:**
```bash
python manage.py collectstatic --noinput
```
Build command এ add করুন।

### Error: "Database connection failed"

**Solution:**
PostgreSQL service restart করুন অথবা SQLite use করুন।

---

## 💰 Railway Free Tier Limits

- **500 hours/month** execution time
- **100 GB** bandwidth
- **1 GB** RAM per service
- **Unlimited** projects

**Calculation:**
- 1 service × 24 hours × 30 days = 720 hours
- 3 services (web + worker + beat) = 240 hours/month
- ✅ Free tier এ চলবে!

---

## 📊 Cost Estimate

### Free Tier (Recommended for testing):
- Web Service: Free
- Redis: Free
- PostgreSQL: Free
- Total: **$0/month**

### Paid (If needed):
- Web Service: $5/month
- Redis: $5/month
- PostgreSQL: $5/month
- Total: **$15/month**

---

## 🎯 Final Checklist

- [ ] Railway account created
- [ ] GitHub repository connected
- [ ] Environment variables added
- [ ] Redis added
- [ ] PostgreSQL added (optional)
- [ ] Deployment successful
- [ ] URL working
- [ ] Email test successful
- [ ] Mobile mail received

---

## 🔗 Useful Links

- Railway Dashboard: https://railway.app/dashboard
- Railway Docs: https://docs.railway.app/
- Your GitHub Repo: https://github.com/Raihanroo/Celer-Scheduler-from-Single-Email-message-transfer-to-Multiple-Email-after-3-minit-

---

## 📱 Support

যদি কোন সমস্যা হয়:
1. Railway logs check করুন
2. Environment variables verify করুন
3. GitHub repository updated আছে কিনা check করুন

**Good luck with deployment! 🚀**
