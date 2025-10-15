import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email():
    # --- 1. 설정 파일 및 데이터 파일 읽기 ---
    try:
        with open('mail_config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        with open('data_to_send.txt', 'r', encoding='utf-8') as f:
            data_content = f.read()
    except FileNotFoundError as e:
        print(f"Error: 필요한 파일을 찾을 수 없습니다 - {e}")
        return

    # --- 2. JSON 파일에서 민감 정보 직접 가져오기 (보안에 매우 취약!) ---
    smtp_user = config.get('smtp_user')
    smtp_password = config.get('smtp_password')

    if not smtp_user or not smtp_password:
        print("Error: mail_config.json 파일에 'smtp_user' 또는 'smtp_password'가 없습니다.")
        return

    # --- 3. 이메일 메시지 구성 ---
    msg = MIMEMultipart('alternative')
    msg['Subject'] = config['subject']
    msg['From'] = smtp_user
    msg['To'] = ", ".join(config['recipients'])

    html_body = f"""
    <html>
    <body>
        <h2>{config['mail_title']}</h2>
        <p>자동화 시스템을 통해 아래 내용을 발송합니다:</p>
        <pre style="background-color:#f4f4f4; border:1px solid #ddd; padding:10px;">{data_content}</pre>
        <p>감사합니다.</p>
    </body>
    </html>
    """
    
    part = MIMEText(html_body, 'html')
    msg.attach(part)

    # --- 4. SMTP 서버를 통해 이메일 발송 ---
    try:
        with smtplib.SMTP(config['smtp_server'], config['smtp_port']) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.sendmail(smtp_user, config['recipients'], msg.as_string())
            print("성공적으로 이메일을 발송했습니다!")
    except Exception as e:
        print(f"이메일 발송 중 오류가 발생했습니다: {e}")

if __name__ == "__main__":
    send_email()