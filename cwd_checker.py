import datetime
import time
import threading
from sqlalchemy import create_engine, Column, Integer, Sequence, String, DateTime, desc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import *
from sqlalchemy import func
from models.cwdlogs import *
from models import dataaccess
import logging
import sys
from configuration import *
from utils.alarmsender import *

FORMAT = "%(asctime)s %(levelname)s %(message)s"
logging.basicConfig(format=FORMAT, level=logging.WARNING)

Base = declarative_base()


class AlarmProcessor(threading.Thread):
    def __init__(self, group=None, target=None, name=None,
                 kwargs=None, verbose=None):
        threading.Thread.__init__(self, group=group, target=target, name=name, verbose=verbose)

        self.db = create_engine(DATABASEURI)
        Session = sessionmaker(bind=self.db)
        self.session = Session()
        self.run_event = kwargs['run_event']

    def run(self):
        while self.run_event.is_set():
            logging.debug("Checking for latents.")
            self.processlatents()
            time.sleep(60)

        logging.critical("Exiting AlarmHandler")


    def processlatents(self):
        jobstatus = self.session.query(JobLog.name,
                                  func.max(JobLog.eventtime).label("lasteventtime"),
                                  JobLog.runtime,
                                  Jobs.period,
                                  Jobs.sla,
                                  Jobs.active).filter(JobLog.name == Jobs.name)\
            .filter(Jobs.active)\
            .group_by(JobLog.name)

        eventname = 'latent_run'

        for js in jobstatus:
            td = datetime.datetime.now() - js.lasteventtime
            perioddelay = int(td.total_seconds() / 60)

            logging.debug('{0} - {1} - {2}'.format(js.name, perioddelay, (js.period + 2*js.sla)))

            #Late/missed job
            if perioddelay > (js.period + 2*js.sla):
                try:
                    alarm = self.session.query(Alarms).filter(Alarms.name == js.name).one()
                    alarm.raisedevent = eventname
                    self.session.commit()

                except NoResultFound:
                    logging.critical('Job {0} is {1} minutes latent. Setting alarm.'.format(js.name, perioddelay))
                    alarm = Alarms(name=js.name, eventtime=datetime.datetime.now(), raisedevent=eventname)
                    self.session.add(alarm)
                    self.session.commit()

                    toemails = dataaccess.getalertemails(self.session, js.name)

                    sendalarm(js.name, eventname, toemails)

if __name__ == '__main__':
    run_event = threading.Event()
    run_event.set()

    ap = AlarmProcessor(name='AlarmProcessor', kwargs={'run_event': run_event})

    logging.warning('Starting CWD Alarm processor.')
    ap.start()

    try:
        while 1:
            time.sleep(.5)
    except KeyboardInterrupt:
        logging.critical("Keyboard Interrupt. Closing Threads")
        run_event.clear()
        ap.join()
        logging.critical("Threads closed. Exiting.")
        exit(1)
