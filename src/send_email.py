import  ssl
import smtplib
from email.message import EmailMessage
from pathlib import Path
import os

context = ssl.create_default_context()    

def send_email(subject, body, receiver, attachment=False):

    # Create a secure SSL context
    msg = EmailMessage()

    msg['Subject'] = subject
    msg['From'] = os.getenv('SENDER_EMAIL')
    msg['To'] = ", ".join(receiver)

    msg.set_content(body)

    if attachment:
        letter_head = Path("./letterhead/populated.pdf")
        with letter_head.open("rb") as fp:
            msg.add_attachment(
                        fp.read(),
                        maintype="image", subtype="png",
                        filename=letter_head.name)
            
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as s:
        s.login(os.getenv('SENDER_EMAIL'), os.getenv('SENDER_PASSWORD'))
        s.send_message(msg)

    return True
    