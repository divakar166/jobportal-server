import os
import requests

RESEND_API_KEY = os.getenv("RESEND_API_KEY")
DOMAIN_NAME = os.getenv("DOMAIN")

def send_verification_email(email, token, user_type):
  confirm_link = f"https://{DOMAIN_NAME}/auth/new-verification?token={token}&type={user_type}"
  url = "https://api.resend.com/emails"
  headers = {
    "Authorization": f"Bearer {RESEND_API_KEY}",
    "Content-Type": "application/json"
  }
  payload = {
    "from": "info@divakarsingh.online",
    "to": email,
    "subject": "Connect - Confirm your email",
    "html": f"<p>Click <a href='{confirm_link}'>here</a> to confirm your email.</p>"
  }
  response = requests.post(url, json=payload, headers=headers)
  return response.status_code, response.json()
