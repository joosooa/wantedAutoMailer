# send_email.py

import os
import smtplib
import json  # json 라이브러리 추가
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# --- (기존의 이메일, 비밀번호 가져오는 부분은 동일) ---
sender_email = os.getenv('GMAIL_USERNAME')
sender_password = os.getenv('GMAIL_PASSWORD')
# recipient_email = os.getenv('RECIPIENT_EMAIL') # <- 이 부분은 JSON에서 읽어올 것이므로 주석 처리하거나 삭제

# JSON 파일 열기
try:
    with open('email_content.json', 'r', encoding='utf-8') as f:
        email_data = json.load(f)
except FileNotFoundError:
    print("❌ 오류: email_content.json 파일을 찾을 수 없습니다.")
    exit(1)

# JSON에서 정보 가져오기
subject = email_data['subject']
body = email_data['body']
recipients = email_data['recipients'] # 받는 사람 목록

if not all([sender_email, sender_password]):
    print("오류: GMAIL_USERNAME 또는 GMAIL_PASSWORD를 설정해야 합니다.")
    exit(1)

# --- (이메일 보내는 로직은 거의 동일, 받는 사람 부분만 수정) ---
try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)

    # 받는 사람 목록(recipients)에 있는 모든 사람에게 이메일 발송
    for recipient in recipients:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        server.sendmail(sender_email, recipient, msg.as_string())
        print(f"✅ 성공: {recipient} 주소로 이메일을 보냈습니다.")

except Exception as e:
    print(f"❌ 오류: 이메일을 보내는 중 문제가 발생했습니다.\n{e}")

finally:
    if 'server' in locals() and server:
        server.quit()
