from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Rawlog(Base):
    __tablename__ = 'rawlog'
    __table_args__ = {'sqlite_autoincrement': True}
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    eventtime = Column(DateTime)
    status = Column(String(8))

class CurrentJobs(Base):
    __tablename__ = 'currentlogs'
    __table_args__ = {'sqlite_autoincrement': True}
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    eventtime = Column(DateTime)
    status = Column(String(8))

class JobLog(Base):
    __tablename__ = 'joblog'
    __table_args__ = {'sqlite_autoincrement': True}
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    eventtime = Column(DateTime)
    status = Column(String(8))
    runtime = Column(Integer)

class Jobs(Base):
    __tablename__ = 'jobs'
    name = Column(String(50), primary_key=True)
    period = Column(Integer)
    sla = Column(Integer)
    active = Column(Boolean)
    description = Column(String(255))

class Alarms(Base):
    __tablename__ = 'alarms'
    __table_args__ = {'sqlite_autoincrement': True}
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    eventtime = Column(DateTime)
    raisedevent = Column(String(50))

class Email(Base):
    __tablename__ = 'emails'
    __table_args__ = {'sqlite_autoincrement': True}
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    emailaddress = Column(String(50))
    namematch = Column(String(50))
    active = Column(Boolean)

