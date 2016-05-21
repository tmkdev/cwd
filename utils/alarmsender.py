import datetime
import logging

from emailer import *

def sendalarm(name, status, toemails):
    statusdict={
        'fail': 'Failed',
        'latent_run': 'Late',
        'sla': 'Runtime Exceeded',
        'ok': 'OK'
    }

    subject = 'CronWatchDog alert: {0} - {1}'.format(name, statusdict[status])
    body = 'Job {0} is now {1}.\r\n{2}\r\nPlease Check.\r\n'.format(name, statusdict[status], datetime.datetime.now())

    logging.warning('Sending alert {0} to {1}'.format(subject, ', '.join(toemails)))

    if len(toemails) > 0:
        sendemail(toemails, subject, body)
