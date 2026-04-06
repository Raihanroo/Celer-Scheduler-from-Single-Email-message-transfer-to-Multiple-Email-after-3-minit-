"""
API Test Script
এই script দিয়ে API test করতে পারবেন
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_schedule_email():
    """Schedule email test"""
    print("\n📧 Testing Schedule Email API...")
    
    url = f"{BASE_URL}/api/schedule-email/"
    data = {
        "emails": [
            "test1@example.com",
            "test2@example.com",
            "test3@example.com"
        ],
        "subject": "Test Scheduled Email",
        "message": "এটি একটি test message। প্রতি 3 মিনিট পর এই mail যাবে।",
        "interval_minutes": 3
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"❌ Error: {e}")


def test_send_immediate():
    """Immediate email test"""
    print("\n🚀 Testing Send Immediate Email API...")
    
    url = f"{BASE_URL}/api/send-email/"
    data = {
        "emails": [
            "test1@example.com",
            "test2@example.com"
        ],
        "subject": "Test Immediate Email",
        "message": "এই mail টি এখনই পাঠানো হবে।"
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"❌ Error: {e}")


def test_email_history():
    """Email history test"""
    print("\n📊 Testing Email History API...")
    
    url = f"{BASE_URL}/api/email-history/"
    
    try:
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"❌ Error: {e}")


def test_scheduled_emails():
    """Scheduled emails list test"""
    print("\n📋 Testing Scheduled Emails List API...")
    
    url = f"{BASE_URL}/api/scheduled-emails/"
    
    try:
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    print("=" * 60)
    print("Email Scheduler API Test")
    print("=" * 60)
    
    print("\n⚠️  নোট: Server চালু আছে কিনা check করুন!")
    print("   python manage.py runserver")
    print("   celery -A core worker --loglevel=info --pool=solo")
    print("   celery -A core beat --loglevel=info")
    
    choice = input("\nকোন test চালাতে চান? (1-5 অথবা 'all'): ")
    
    if choice == "1":
        test_schedule_email()
    elif choice == "2":
        test_send_immediate()
    elif choice == "3":
        test_email_history()
    elif choice == "4":
        test_scheduled_emails()
    elif choice.lower() == "all":
        test_schedule_email()
        test_send_immediate()
        test_email_history()
        test_scheduled_emails()
    else:
        print("\n❌ Invalid choice!")
        print("\nOptions:")
        print("1 - Schedule Email")
        print("2 - Send Immediate Email")
        print("3 - Email History")
        print("4 - Scheduled Emails List")
        print("all - Run all tests")
