# 🚀 Render Deployment Guide - Step by Step

এই guide follow করে আপনি সহজেই Render এ deploy করতে পারবেন।

---

## 📋 Pre-requisites

- ✅ GitHub account
- ✅ Render account (free)
- ✅ Gmail App Password

---

## Step 1: পুরনো Service Delete করুন (যদি থাকে)

1. Render Dashboard এ যান: https://dashboard.render.com/
2. Left sidebar → "Pre_Industry_Program" select করুন
3. Left sidebar → "Settings" click করুন
4. নিচে scroll করে "Delete Web Service" button click করুন
5. Service name টাইপ করে confirm করুন

---

## Step 2: নতুন Web Service তৈরি করুন

### 2.1 Dashboard এ যান
- https://dashboard.render.com/

### 2.2 New Web Service তৈরি করুন
1. উপরে "New +" button click করুন
2. "Web Service" select করুন

### 2.3 GitHub Repository Connect করুন
1. "Connect a repository" section এ যান
2. যদি প্রথমবার হয়, "Connect GitHub" click করুন
3. আপনার repository খুঁজুন:
   ```
   Celer-Scheduler-from-Single-Email-message-transfer-to-Multiple-Email-after-3-minit-
   ```
4. "Connect" button click করুন

---

## Step 3: Service Configuration

এখন একটা form আসবে। নিচের মতো fill করুন:

### Basic Settings:

**Name:**
```
django-email-scheduler
```

**Region:**
```
Singapore (বা যেকোনো কাছের region)
```

**Branch:**
```
main
```

**Runtime:**
```
Python 3
```

### Build & Deploy Settings:

**Build Command:**
```bash
chmod +x build.sh && ./build.sh
```

**Start Command:**
```bash
gunicorn core.wsgi:application
```

### Instance Type:
```
Free (select করুন)
```

---

## Step 4: Environment Variables Add করুন

"Advanced" section expand করুন এবং "Add Environment Variable" click করুন।

নিচের variables একটা একটা করে add করুন:

### 4.1 SECRET_KEY
```
Key: SECRET_KEY
Value: django-insecure-f1imqkk^iy^kx#@mua!3al#^m@83-r7zr58t^!%$7h&$kp6s14
```
(অথবা নতুন generate করুন: https://djecrety.ir/)

### 4.2 DEBUG
```
Key: DEBUG
Value: False
```

### 4.3 EMAIL_HOST_USER
```
Key: EMAIL_HOST_USER
Value: raihanroo21@gmail.com
```

### 4.4 EMAIL_HOST_PASSWORD
```
Key: EMAIL_HOST_PASSWORD
Value: bcvklomzstrcxzzc
```

### 4.5 ALLOWED_HOSTS (Optional)
```
Key: ALLOWED_HOSTS
Value: .onrender.com
```

---

## Step 5: Create Web Service

1. সব configuration check করুন
2. নিচে "Create Web Service" button click করুন
3. Deployment শুরু হবে (5-10 minutes লাগতে পারে)

---

## Step 6: Deployment Monitor করুন

### 6.1 Build Logs দেখুন
- Automatically logs দেখাবে
- নিচের messages দেখবেন:
  ```
  ==> Installing dependencies
  ==> Running build command
  ==> Collecting static files
  ==> Running migrations
  ==> Build successful
  ```

### 6.2 Deploy Status
- উপরে দেখবেন: "Live" (green)
- URL পাবেন: `https://django-email-scheduler.onrender.com`

---

## Step 7: Test Your Deployment

### 7.1 Open Your Site
1. URL click করুন অথবা browser এ paste করুন
2. Email form দেখতে পাবেন

### 7.2 Send Test Email
1. Email address add করুন
2. Subject এবং Message লিখুন
3. "Send Now" button click করুন
4. Email check করুন

---

## 🎯 Scheduled Emails Setup (Optional)

Render এ scheduled emails চালানোর জন্য:

### Option 1: Background Worker (Paid)
1. Dashboard → "New +" → "Background Worker"
2. Same repository select করুন
3. Start Command:
   ```bash
   python manage.py send_scheduled_emails --interval=60
   ```

### Option 2: Cron Job (Free)
1. Dashboard → "New +" → "Cron Job"
2. Schedule: `*/5 * * * *` (every 5 minutes)
3. Command:
   ```bash
   python manage.py send_scheduled_emails --once
   ```

---

## 🔧 Troubleshooting

### Build Failed?

**Check Build Logs:**
- Scroll করে error message খুঁজুন
- Common issues:
  - Missing dependencies → requirements.txt check করুন
  - Migration errors → Database connection check করুন

**Solution:**
1. GitHub এ code fix করুন
2. Push করুন
3. Render automatically re-deploy করবে

### Site Not Loading?

**Check:**
1. Deployment status "Live" আছে কিনা
2. Logs এ error আছে কিনা
3. Environment variables সঠিক আছে কিনা

**View Logs:**
- Dashboard → Your Service → "Logs" tab

### Emails Not Sending?

**Check:**
1. Environment variables:
   - EMAIL_HOST_USER সঠিক
   - EMAIL_HOST_PASSWORD সঠিক (16 digits)
2. Gmail App Password active আছে
3. Logs এ email errors দেখুন

---

## 📊 Monitor Your App

### View Logs:
```
Dashboard → Your Service → Logs
```

### View Metrics:
```
Dashboard → Your Service → Metrics
```

### View Events:
```
Dashboard → Your Service → Events
```

---

## 🔄 Update Your App

যখন code update করবেন:

1. Local এ changes করুন
2. Git commit করুন:
   ```bash
   git add .
   git commit -m "Update message"
   git push origin main
   ```
3. Render automatically detect করে re-deploy করবে

---

## 💡 Important Notes

### Free Tier Limitations:
- ⚠️ 15 minutes inactivity এর পর sleep mode এ যায়
- ⚠️ প্রথম request এ 50 seconds delay হতে পারে
- ⚠️ 750 hours/month free (1 service এর জন্য যথেষ্ট)

### Keep Service Active:
- UptimeRobot ব্যবহার করুন (free)
- প্রতি 5 minutes এ ping করবে
- Service awake থাকবে

---

## ✅ Success Checklist

- [ ] পুরনো service delete করেছি
- [ ] নতুন web service তৈরি করেছি
- [ ] GitHub repository connect করেছি
- [ ] Build command সঠিক দিয়েছি
- [ ] Start command সঠিক দিয়েছি
- [ ] সব environment variables add করেছি
- [ ] Deployment successful (Live status)
- [ ] Site খুলছে
- [ ] Test email পাঠিয়েছি
- [ ] Email পেয়েছি

---

## 🎉 Congratulations!

আপনার Django Email Scheduler এখন live!

**Your URL:**
```
https://django-email-scheduler.onrender.com
```

Share করুন এবং use করুন! 📧

---

## 📞 Need Help?

যদি কোনো সমস্যা হয়:
1. Build logs check করুন
2. Environment variables verify করুন
3. GitHub এ latest code আছে কিনা check করুন

**Happy Deploying! 🚀**
