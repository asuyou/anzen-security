import smtplib
import datetime
from email.mime.text import MIMEText

class EmailClient:
    def __init__(self, sender_email: str, server: str, port: int) -> None:
        print("Start 1")
        smtp = smtplib.SMTP(host=server, port=port)

        print("connected")

        smtp.ehlo()
        smtp.starttls()

        print("tls on")

        self.sender_email = sender_email

        self.smtp = smtp

    def login(self, user: str, password: str):
        self.smtp.login(user=user, password=password)
        print("Logged in")

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
            print("Sent email")
        except Exception as e:
            print("Unable to send email. Are you connected to the email server?")
            print(e)
            

if __name__ == "__main__":
    client = EmailClient("Security <anzen@asyo.dev>", "email-smtp.eu-west-2.amazonaws.com", 587)
    client.login("AKIAYT7FJXDURUVBJWNF", "BLylydG99rOyAy49Bt8r4OXxhUZiAY/qC3q5lFQHXWiD")
    client.send_email(["Asyo <a@asyo.dev>"], "Testing SMPT Auto", "This is a security test")

