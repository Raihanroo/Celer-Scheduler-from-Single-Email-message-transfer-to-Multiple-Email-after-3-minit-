# 🚀 PythonAnywhere Deployment Guide

## ধাপে ধাপে PythonAnywhere এ Deploy করার সম্পূর্ণ গাইড

---

## ধাপ ১: PythonAnywhere Account তৈরি করুন

### 1.1 Website এ যান
```
https://www.pythonanywhere.com/
```

### 1.2 Sign Up করুন
- **"Start running Python online in less than a minute"** button এ click করুন
- **"Create a Beginner account"** select করুন (Free)
- Username, Email, Password দিন
- Email verify করুন

---

## ধাপ ২: Bash Console খুলুন

### 2.1 Dashboard এ যান
- Login করার পর dashboard দেখবেন

### 2.2 Console খুলুন
- **"Consoles"** tab এ click করুন
- **"Bash"** select করুন
- একটি terminal window খুলবে

---

## ধাপ ৩: GitHub থেকে Code Clone করুন

### 3.1 Bash console এ commands run করুন:

```bash
# Home directory তে যান
cd ~

# GitHub repository clone করুন
git clone https://github.com/Raihanroo/Celer-Scheduler-from-Single-Email-message-transfer-to-Multiple-Email-after-3-minit-.git

# Project directory তে যান
cd Celer-Scheduler-from-Single-Email-message-transfer-to-Multiple-Email-after-3-minit-

# Check করুন files আছে কিনা
ls -la
```

---

## ধাপ ৪: Virtual Environment তৈরি করুন

### 4.1 Virtual environment তৈরি করুন:

```bash
# Python 3.11 দিয়ে virtual environment তৈরি
python3.11 -m venv venv

# Virtual environment activate করুন
source venv/bin/activate

# Pip upgrade করুন
pip install --upgrade pip
```

### 4.2 Dependencies install করুন:

```bash
# Requirements install করুন
pip install -r requirements.txt

# Django check করুন
python manage.py --version
```

---

## ধাপ ৫: Environment Variables Setup

### 5.1 .env file তৈরি করুন:

```bash
# .env file তৈরি করুন
nano .env
```

### 5.2 এই content paste করুন:

```env
SECRET_KEY=your-secret-key-here-generate-new-one
DEBUG=False
ALLOWED_HOSTS=.pythonanywhere.com
EMAIL_HOST_USER=raihanroo21@gmail.com
EMAIL_HOST_PASSWORD=bcvklomzstrcxzzc
DATABASE_NAME=db.sqlite3
```

**Save করুন:** `Ctrl + X`, তারপর `Y`, তারপর `Enter`

### 5.3 Secret Key Generate করুন:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy করে `.env` file এ `SECRET_KEY` এ paste করুন।

---

## ধাপ ৬: Database Setup

### 6.1 Database migrate করুন:

```bash
# Migrations run করুন
python manage.py migrate

# Superuser তৈরি করুন
python manage.py createsuperuser
```

Username, Email, Password দিন।

### 6.2 Static files collect করুন:

```bash
python manage.py collectstatic --noinput
```

---

## ধাপ ৭: Web App Configure করুন

### 7.1 Web tab এ যান
- Dashboard → **"Web"** tab
- **"Add a new web app"** button click করুন

### 7.2 Configuration:
1. **"Next"** click করুন
2. **"Manual configuration"** select করুন
3. **Python 3.11** select করুন
4. **"Next"** click করুন

---

## ধাপ ৮: WSGI File Configure করুন

### 8.1 WSGI file edit করুন:
- Web tab এ **"WSGI configuration file"** link এ click করুন
- সব content delete করুন

### 8.2 এই code paste করুন:

```python
import os
import sys

# Project path
path = '/home/YOUR_USERNAME/Celer-Scheduler-from-Single-Email-message-transfer-to-Multiple-Email-after-3-minit-'
if path not in sys.path:
    sys.path.insert(0, path)

# Virtual environment
venv_path = '/home/YOUR_USERNAME/Celer-Scheduler-from-Single-Email-message-transfer-to-Multiple-Email-after-3-minit-/venv'
activate_this = os.path.join(venv_path, 'bin', 'activate_this.py')

# Load environment variables
from dotenv import load_dotenv
env_path = os.path.join(path, '.env')
load_dotenv(env_path)

# Django settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings'

# WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

**Important:** `YOUR_USERNAME` replace করুন আপনার PythonAnywhere username দিয়ে!

**Save করুন:** `Ctrl + S` অথবা Save button

---

## ধাপ ৯: Virtual Environment Path Set করুন

### 9.1 Web tab এ scroll করুন
- **"Virtualenv"** section খুঁজুন
- **"Enter path to a virtualenv"** field এ paste করুন:

```
/home/YOUR_USERNAME/Celer-Scheduler-from-Single-Email-message-transfer-to-Multiple-Email-after-3-minit-/venv
```

**Important:** `YOUR_USERNAME` replace করুন!

---

## ধাপ ১০: Static Files Configure করুন

### 10.1 Static files mapping:
- Web tab এ **"Static files"** section এ যান
- **"Enter URL"** এ লিখুন: `/static/`
- **"Enter path"** এ লিখুন:

```
/home/YOUR_USERNAME/Celer-Scheduler-from-Single-Email-message-transfer-to-Multiple-Email-after-3-minit-/staticfiles
```

---

## ধাপ ১১: Reload Web App

### 11.1 Web app reload করুন:
- Web tab এর top এ **"Reload"** button (green) click করুন
- Wait করুন 10-20 seconds

### 11.2 আপনার website খুলুন:
```
https://YOUR_USERNAME.pythonanywhere.com
```

---

## ✅ Success! আপনার Website Live!

আপনার Django Email Scheduler এখন live:
```
https://YOUR_USERNAME.pythonanywhere.com
```

---

## 🔧 Troubleshooting

### Error দেখলে:

#### 1. Error Log দেখুন:
- Web tab → **"Log files"** section
- **"Error log"** click করুন
- শেষের errors দেখুন

#### 2. Common Issues:

**ImportError: No module named 'dotenv'**
```bash
source venv/bin/activate
pip install python-dotenv
```

**Static files না দেখালে:**
```bash
python manage.py collectstatic --noinput
```

**Database error:**
```bash
python manage.py migrate
```

---

## 📝 Important Notes

### Free Account Limitations:
- ✅ 1 web app
- ✅ 512 MB disk space
- ✅ Daily CPU limit
- ❌ No Celery (scheduled emails won't work)
- ❌ No custom domain (paid feature)

### What Will Work:
- ✅ Web UI
- ✅ Immediate email sending
- ✅ Email history
- ✅ Admin panel
- ✅ API endpoints

### What Won't Work (Free tier):
- ❌ Scheduled emails (Celery)
- ❌ Background tasks
- ❌ Celery Beat

---

## 🎯 Next Steps

### 1. Test Your Website:
```
https://YOUR_USERNAME.pythonanywhere.com
```

### 2. Admin Panel:
```
https://YOUR_USERNAME.pythonanywhere.com/admin
```

### 3. Send Test Email:
- Open website
- Add email addresses
- Click "Send Now"
- Check your inbox

---

## 🔄 Update করার নিয়ম

যখন code update করবেন:

```bash
# Bash console এ
cd ~/Celer-Scheduler-from-Single-Email-message-transfer-to-Multiple-Email-after-3-minit-

# Latest code pull করুন
git pull origin main

# Virtual environment activate করুন
source venv/bin/activate

# Dependencies update করুন
pip install -r requirements.txt

# Migrations run করুন
python manage.py migrate

# Static files collect করুন
python manage.py collectstatic --noinput

# Web app reload করুন (Web tab থেকে)
```

---

## 💡 Tips

1. **Keep your .env secure** - GitHub এ push করবেন না
2. **Regular backups** - Database backup নিন
3. **Monitor logs** - Error logs regularly check করুন
4. **Test locally first** - Deploy করার আগে local এ test করুন

---

## 🎉 Congratulations!

আপনার Django Email Scheduler এখন live এবং accessible!

**Share করুন:**
```
https://YOUR_USERNAME.pythonanywhere.com
```

---

## 📞 Support

- PythonAnywhere Help: https://help.pythonanywhere.com/
- PythonAnywhere Forums: https://www.pythonanywhere.com/forums/
- Django Docs: https://docs.djangoproject.com/

---

**Happy Deploying! 🚀**
