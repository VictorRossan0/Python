import smtplib
import traceback
from dotenv.main import load_dotenv
import os

class Email:

    @staticmethod
    def send_error_email(error_message):
        # Email server configuration
        smtp_server = os.environ['MAIL_HOST']
        smtp_port = os.environ['MAIL_PORT']
        sender_email = os.environ['MAIL_USERNAME']
        sender_password = os.environ['MAIL_PASSWORD']
        recipient_email = os.environ['MAIL_FROM_ADDRESS']

        # Compose the email message
        subject = 'Error in Python Script'
        body = f"An error occurred:\n\n{error_message}\n\nTraceback:\n{traceback.format_exc()}"

        message = f"Subject: {subject}\n\n{body}"

        try:
            # Establish a secure connection with the SMTP server
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()

            # Login to your email account
            server.login(sender_email, sender_password)

            # Send the email
            server.sendmail(sender_email, recipient_email, message)
            print('Error email sent successfully!')

        except Exception as e:
            print(f'Error sending email: {str(e)}')

        finally:
            # Close the connection
            server.quit()