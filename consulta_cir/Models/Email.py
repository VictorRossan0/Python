import smtplib  # Importa o módulo smtplib para enviar e-mails
import traceback  # Importa o módulo traceback para obter informações sobre exceções
from dotenv.main import load_dotenv  # Importa a função load_dotenv do módulo dotenv
import os  # Importa o módulo os para acessar variáveis de ambiente

class Email:

    @staticmethod
    def send_error_email(error_message):
        # Carrega as variáveis de ambiente do arquivo .env
        load_dotenv()
        # Configuração do servidor de e-mail
        smtp_server = os.environ['MAIL_HOST']
        smtp_port = os.environ['MAIL_PORT']
        sender_email = os.environ['MAIL_USERNAME']
        sender_password = os.environ['MAIL_PASSWORD']
        recipient_email = os.environ['MAIL_FROM_ADDRESS']

        # Composição da mensagem de e-mail
        subject = 'Error in Python Script'
        body = f"An error occurred:\n\n{error_message}\n\nTraceback:\n{traceback.format_exc()}"

        message = f"Subject: {subject}\n\n{body}"

        try:
            # Estabelece uma conexão segura com o servidor SMTP
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()

            # Login na conta de e-mail
            server.login(sender_email, sender_password)

            # Envio do e-mail
            server.sendmail(sender_email, recipient_email, message)
            print('Error email sent successfully!')

        except Exception as e:
            print(f'Error sending email: {str(e)}')

        finally:
            # Fecha a conexão
            server.quit()
