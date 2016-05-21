from configuration import *
from models.cwdlogs import *
from models.dataaccess import *
from utils.alarmsender import *
from logging import *
from sqlalchemy.orm.exc import *


def delcurrent(db, name):
    db.query(CurrentJobs).filter(CurrentJobs.name == name).delete()
    db.commit()


def clearalarm(db,name):
    try:
        db.query(Alarms).filter(Alarms.name == name).one()
        sendalarm(name, 'ok')
        db.query(Alarms).filter(Alarms.name == name).delete()
        db.commit()
    except NoResultFound:
        pass


def raisealarm(db, name, raisedevent):
    try:
        db.query(Alarms).filter(Alarms.name == name).one().\
            update({"raisedevent": raisedevent})

    except NoResultFound:
        toemails = getalertemails(db, name)

        sendalarm(name, raisedevent, toemails)
        alarm = Alarms(name=name, eventtime=datetime.datetime.now(), raisedevent=raisedevent)
        db.add(alarm)

    db.commit()


def checkauth(username, password):
    if username == ADMINUSER and password == ADMINPASS:
        return True
    return False
