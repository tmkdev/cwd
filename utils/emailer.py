import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging

from configuration import *


def sendemail(to_emails, subject, textbody, htmlbody=None):
    to = ', '.join(to_emails)
    textbody += '\n\n'

    if len(to_emails) == 0:
        logging.error('Not sending email to empty to.')
        return False

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = CWDPAGEEMAIL
    msg['To'] = to

    part1 = MIMEText(textbody, 'plain')
    msg.attach(part1)

    if htmlbody is not None:
        part2 = MIMEText(htmlbody, 'html')
        msg.attach(part2)

    try:
        server = smtplib.SMTP(SMTPSERVER, SMTPPORT)
        server.set_debuglevel(False)
        server.starttls()
        server.login(SMTPUSER, SMTPPASSWORD)

        server.sendmail(CWDPAGEEMAIL, to, msg.as_string())
        server.quit()
        return True
    except:
        logging.critical('Email send failed.')
        return False


if __name__ == '__main__':
    sendemail(['test@null.com'], 'CronWatchDog alert', 'Job 123 failed.')