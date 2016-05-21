import datetime
from cwdlogs import *
from sqlalchemy.orm.exc import *
from sqlalchemy import func
from models.cwdlogs import *
import logging
from sqlalchemy import create_engine, Column, Integer, Sequence, String, DateTime, desc, and_, or_


def jobstatuses(dbsession, dateback=datetime.datetime.now()-datetime.timedelta(days=30)):

    results = {}
    statuses = ['end', 'fail']

    jobstatus = dbsession.query(JobLog.status,
                                func.date(JobLog.eventtime).label('eventday'),
                                func.count('*').label('count')).\
        filter(JobLog.eventtime > dateback).\
        group_by(JobLog.status, func.date(JobLog.eventtime))

    for j in jobstatus:
        if j.eventday not in results:
            results[j.eventday] = {}
            for status in statuses:
                results[j.eventday][status]=0
        results[j.eventday][j.status] = j.count


    return results


def jobsummary(dbsession, dateback=datetime.datetime.now()-datetime.timedelta(days=1)):
    results = {'fail': 0, 'end': 0, 'current': 0, 'alarm': 0}

    jobstatus = dbsession.query(JobLog.status,
                                func.count('*').label('count')). \
        filter(JobLog.eventtime > dateback). \
        group_by(JobLog.status)

    for j in jobstatus:
        results[j.status] = j.count

    results['current'] = dbsession.query(CurrentJobs).count()
    results['alarm'] = dbsession.query(Alarms).count()

    return results


def joblog(dbsession, last=10, name=None):
    joblog = dbsession.query(JobLog).order_by(desc(JobLog.eventtime))

    if name is not None:
        joblog = joblog.filter(JobLog.name == name)

    joblog = joblog.limit(last)

    return joblog


def joblogsummary(dbsession):

    subq = dbsession.query(JobLog.name, func.max(JobLog.runtime).label('maxruntime'),
                            func.min(JobLog.runtime).label('minruntime'),
                            func.max(JobLog.eventtime).label('last_eventtime'))\
                .group_by(JobLog.name).subquery()

    jobs = dbsession.query(JobLog.name, JobLog.eventtime, JobLog.runtime, JobLog.status,
                                subq,
                                Jobs.sla, Jobs.period, Jobs.active).join(subq, and_(JobLog.name == subq.c.name,
                                                    JobLog.eventtime == subq.c.last_eventtime)).\
            outerjoin(Jobs, Jobs.name == JobLog.name).\
            order_by(desc(JobLog.eventtime))

    return jobs


def landingtimes(dbsession, jobname, starttime, endtime):

    results = dbsession.query(JobLog).filter(JobLog.name == jobname)\
        .filter(JobLog.eventtime.between(starttime, endtime))\
        .order_by(desc(JobLog.eventtime))

    return results


def runningjobs(dbsession):
    result = dbsession.query(CurrentJobs)
    return result


def activealarms(dbsession):
    result = dbsession.query(Alarms)
    return result


def emaillist(dbsession):
    result = dbsession.query(Email)
    return result


def getemail(dbsession, id):
    try:
        email = dbsession.query(Email).filter(Email.id == id).one()
    except NoResultFound:
        return None
    return email


def deleteemail(dbsession, id):
    dbsession.query(Email).filter(Email.id == id).delete()
    dbsession.commit()

    return True


def getjob(dbsession, name):
    try:
        job = dbsession.query(Jobs).filter(Jobs.name == name).one()
        return job
    except NoResultFound:
        return None


def getalertemails(dbsession, jobname):
    results = dbsession.query(Jobs, Email).filter(Jobs.name == jobname)\
        .filter(Email.active)\
        .filter(Jobs.active)\
        .filter(Jobs.name.like(Email.namematch))

    emailtolist = []
    for result in results:
        emailtolist.append(result.Email.emailaddress)

    return emailtolist