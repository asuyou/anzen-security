import smtplib
import datetime
from email.mime.text import MIMEText

# Documentation used:
# https://docs.python.org/3/library/smtplib.html

class EmailClient:
    def __init__(self, sender_email: str, server: str, port: int) -> None:
        self.server = server
        self.port = port

        self.sender_email = sender_email

    def login(self, user: str, password: str):
        self.user = user
        self.password = password

    def connect_and_login(self) -> smtplib.SMTP:
        smtp = smtplib.SMTP(host=self.server, port=self.port)
        smtp.ehlo()
        smtp.starttls()
        smtp.login(user=self.user, password=self.password)
        return smtp

    def send_email(self, recipients: list[str], sub: str, message: str):
        smtp = self.connect_and_login()
        current_date_time = datetime.datetime.now().strftime("%Y/%m/%d, %H:%M:%S")

        joined_emails = " ".join(recipients)

        date_body = f"""Date: {current_date_time}

{message}
        """
        email_body = MIMEText(date_body)
        email_body["Subject"] = sub
        
        print(recipients)

        try:
            smtp.sendmail(from_addr=self.sender_email, to_addrs=joined_emails, msg=email_body.as_string())
        except Exception as e:
            print("Unable to send email. Are you connected to the email server?")
            print(e)
            

