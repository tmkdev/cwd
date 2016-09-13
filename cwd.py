import datetime
import time
import logging
import sys
import threading

import bottle
from bottle import HTTPError, template, view, request, static_file, auth_basic, route, redirect, BaseTemplate
from bottle.ext import sqlalchemy
from sqlalchemy.orm.exc import *
from sqlalchemy import create_engine, Column, Integer, Sequence, String, DateTime, desc
from sqlalchemy.ext.declarative import declarative_base

from models.cwdlogs import *
from configuration import *
from utils.emailer import *
from utils.alarmsender import *
from cwd_helpers import *
from models.dataaccess import *


FORMAT = "%(asctime)s %(levelname)s %(message)s"
logging.basicConfig(format=FORMAT, level=logging.INFO)

engine = create_engine(DATABASEURI, echo=False)

app = bottle.Bottle()
plugin = sqlalchemy.Plugin(
    engine, # SQLAlchemy engine created with create_engine function.
    Base.metadata, # SQLAlchemy metadata, required only if create=True.
    keyword='db', # Keyword used to inject session database in a route (default 'db').
    create=True, # If it is true, execute `metadata.create_all(engine)` when plugin is applied (default False).
    commit=True, # If it is true, plugin commit changes after route is executed (default True).
    use_kwargs=False # If it is true and keyword is not defined, plugin uses **kwargs argument to inject session database (default False).
)

app.install(plugin)

BaseTemplate.defaults['get_url'] = app.get_url

statuslookup = {'end': 'Run OK', 'fail': 'Failed', 'latent_run': 'Missing Period', 'sla': 'SLA Time Exceeded'}


@app.route('/jobs', apply=[auth_basic(checkauth)])
def jobsum(db):
    joblogsum=joblogsummary(db)

    output = template('jobsummary', joblist=joblogsum, statuslookup=statuslookup)
    return output


@app.route('/jobs/<name>', apply=[auth_basic(checkauth)])
def jobdetail(db, name):
    starttime = datetime.datetime.now() - datetime.timedelta(days=30)
    endtime = datetime.datetime.now()

    landinglogs = landingtimes(db, name, starttime, endtime)
    jl = joblog(db, last=50, name=name)

    output = template('jobdetail', jobname=name, landinglogs=landinglogs,
                      lastjobs=jl,
                      statuslookup=statuslookup)
    return output

@app.route('/about', apply=[auth_basic(checkauth)])
def about():
    output = template("about")
    return output


@app.route('/', apply=[auth_basic(checkauth)])
def logs(db):
    landingtrend = jobstatuses(db)
    summary = jobsummary(db)
    lastjobs = joblog(db)
    runjobs = runningjobs(db)
    alarms = activealarms(db)

    output = template("overview", landingtrend=landingtrend,
                      summary=summary, lastjobs=lastjobs,
                      runjobs=runjobs, alarms=alarms,
                      statuslookup=statuslookup)
    return output


@app.route('/status/<name>/<status>', method='POST')
def statusupdate(name, status, db):
    try:
        if request.POST.cwd_apikey != API_KEY:
            return {'error': 'API KEY is wrong'}
    except:
        return {'error': 'NO API KEY'}

    if status in ['start', 'end', 'fail']:
        rawlog = Rawlog(name=name, eventtime=datetime.datetime.now(), status=status)
        db.add(rawlog)
        db.commit()

        if status == 'start':
            delcurrent(db, name)
            curjob = CurrentJobs(name=name, eventtime=datetime.datetime.now(), status=status)
            db.add(curjob)
            db.commit()

        if status in ['end', 'fail']:
            runtime = 0

            try:
                thiscurrent = db.query(CurrentJobs).filter(CurrentJobs.name == name).one()
                rt = datetime.datetime.now()-thiscurrent.eventtime
                runtime = int(rt.total_seconds())

                joblog = JobLog(name=name, eventtime=thiscurrent.eventtime, status=status,
                                runtime=runtime)
                db.add(joblog)
                db.commit()
                delcurrent(db, name)

            except NoResultFound:
                logging.error("No current status")
                joblog = JobLog(name=name, eventtime=datetime.datetime.now(), status=status,
                                runtime=runtime)
                db.add(joblog)
                db.commit()


            if status == 'end':
                try:
                    job = db.query(Jobs).filter(Jobs.name == name).one()
                    if runtime > 0 and job.sla > 0 and runtime / 60 > job.sla:
                        raisealarm(db, name, 'sla')
                    else:
                        clearalarm(db, name)
                except NoResultFound:
                    logging.warning('{0} has no sla.'.format(name))
                    clearalarm(db, name)

            if status == 'fail':
                raisealarm(db, name, status)

    return


@app.route('/jobform/<name>', apply=[auth_basic(checkauth)], method=['GET', 'POST'])
def jobform(db, name):
    job = getjob(db, name)

    output = template('jobform', jobname=name, job=job)
    return output


@app.route('/jobedit', apply=[auth_basic(checkauth)], method=['POST'])
def jobedit(db):
    jobname = request.forms.jobname
    job = getjob(db, jobname)

    active = False
    if request.forms.active == 'on':
        active = True

    if job == None:
        newjob = Jobs(name=jobname,
                        period=request.forms.period,
                        sla=request.forms.sla,
                        active=active,
                        description=request.forms.description)

        db.add(newjob)
    else:
        job.period = request.forms.period
        job.sla = request.forms.sla
        job.active = active
        job.description = request.forms.description

    db.commit()
    redirect('/jobs')


@app.route('/email', apply=[auth_basic(checkauth)])
def email(db):
    email_list = emaillist(db)

    output = template('email', emaillist=email_list)
    return output


@app.route('/emaildelete/<id>', apply=[auth_basic(checkauth)])
def emaildelete(db, id):
    deleteemail(db, id)
    return redirect('/email')


@app.route('/emailform', apply=[auth_basic(checkauth)], method=['GET', 'POST'])
@app.route('/emailform/<id>', apply=[auth_basic(checkauth)], method=['GET', 'POST'])
def emailform(db, id=None):
    email = None
    if id is not None:
        email = getemail(db, id)

    if request.method == 'POST':
        active = False
        if request.forms.active == 'on':
            active = True
        if id is None:
            newemail = Email(name=request.forms.name,
                             emailaddress=request.forms.emailaddress,
                             namematch=request.forms.namematch,
                             active=active
                             )

            db.add(newemail)
            db.commit()

            return redirect('/email')

        else:
            email.name = request.forms.name
            email.emailaddress = request.forms.emailaddress
            email.namematch = request.forms.namematch
            email.active = active

            db.add(email)
            db.commit()

            return redirect('/email')

    output = template('emailform', email=email)
    return output


