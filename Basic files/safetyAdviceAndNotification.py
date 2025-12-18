import smtplib
from email.mime.text import MIMEText

def send_email(subject, body, to_email):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = 'your-email@example.com'
    msg['To'] = to_email

    with smtplib.SMTP('smtp.example.com') as server:
        server.login('your-email@example.com', 'your-password')
        server.sendmail(msg['From'], [msg['To']], msg.as_string())