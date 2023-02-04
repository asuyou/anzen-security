import smtplib
import datetime
from email.mime.text import MIMEText

# Documentation used:
# https://docs.python.org/3/library/smtplib.html

class EmailClient:
    def __init__(self, sender_email: str, server: str, port: int) -> None:
        smtp = smtplib.SMTP(host=server, port=port)

        smtp.ehlo()
        smtp.starttls()

        self.sender_email = sender_email

        self.smtp = smtp

    def login(self, user: str, password: str):
        self.smtp.login(user=user, password=password)

    def send_email(self, recipients: list[str], sub: str, message: str):
        current_date_time = datetime.datetime.now().strftime("%Y/%m/%d, %H:%M:%S")

        joined_emails = " ".join(recipients)

        date_body = f"""Date: {current_date_time}

{message}
        """
        email_body = MIMEText(date_body)
        email_body["Subject"] = sub
        
        try:
            self.smtp.sendmail(from_addr=self.sender_email, to_addrs=joined_emails, msg=email_body.as_string())
        except Exception as e:
            print("Unable to send email. Are you connected to the email server?")
            print(e)
            

