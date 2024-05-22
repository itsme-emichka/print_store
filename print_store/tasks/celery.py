import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from celery import Celery

from config import SENDER_EMAIL, SENDER_PASSWORD, REDIS_HOST, REDIS_PORT
from extra.http_exceptions import MailingError


celery = Celery('tasks', broker=f'redis://{REDIS_HOST}:{REDIS_PORT}')


@celery.task
def send_message(
    reciever: str,
    subject: str,
    html_message: str,
) -> bool:
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg['To'] = reciever

    text = MIMEText(html_message, 'html')
    msg.attach(text)

    try:
        smtp = smtplib.SMTP('smtp.yandex.ru', 587)
        smtp.ehlo()
        smtp.starttls()
        smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
        smtp.sendmail(
            from_addr=SENDER_EMAIL,
            to_addrs=reciever,
            msg=msg.as_string(),
        )
        smtp.quit()
        return True
    except Exception as ex:
        print(ex)
        raise MailingError
