import os
import smtplib
from email.mime.text import MIMEText

# Gmail-Daten
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
USERNAME = "eddi.mickan@gmail.com"
APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")

def send_mail():
    msg = MIMEText("Hallo Welt")
    msg["Subject"] = "Testmail"
    msg["From"] = USERNAME
    msg["To"] = USERNAME

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(USERNAME, APP_PASSWORD)
        server.send_message(msg)

if __name__ == "__main__":
    send_mail()
    print("Mail gesendet.")
