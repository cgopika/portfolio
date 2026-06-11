import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

sender = "moaname032@gmail.com"
receiver = "moaname032@gmail.com"

app_password = "soha itka cjya ewon"

with open("news_digest.html", "r", encoding="utf-8") as file:
    html_content = file.read()

msg = MIMEMultipart("alternative")

msg["Subject"] = "📰 Daily News Digest"
msg["From"] = sender
msg["To"] = receiver

html_part = MIMEText(html_content, "html")
msg.attach(html_part)

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login(sender, app_password)
    server.send_message(msg)

print("Email sent successfully!")