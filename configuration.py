import ast
import os
import logging

#EMAIL SERVER SETTINGS
CWDPAGEEMAIL = os.getenv('CWDPAGEEMAIL', 'cronwatchdog@yourdomain.com')  # CWD SEND email address
logging.error('CWDPAGEEMAIL: {0}'.format(CWDPAGEEMAIL))

CWDDOMAIN = os.getenv('CWDDOMAIN', 'yourdomain.com')
logging.error('CWDDOMAIN: {0}'.format(CWDDOMAIN))

SMTPSERVER = os.getenv('SMTPSERVER', 'yoursmtpserver.com')
logging.error('SMTPSERVER: {0}'.format(SMTPSERVER))

SMTPUSER = os.getenv('SMTPUSER', 'yoursmtpuser')             #SMTP User if authentication/SSL is needed
logging.error('SMTPUSER: {0}'.format(SMTPUSER))

SMTPPORT = os.getenv('SMTPPORT', '123')
logging.error('SMTPPORT: {0}'.format(SMTPPORT))

SMTPPASSWORD = os.getenv('SMTPPASSWORD', 'yourpassword')
logging.error('SMTPPASSWORD: {0}'.format(SMTPPORT))

SMTPSSL = ast.literal_eval(os.getenv('SMTPSSL', 'True'))
logging.error('SMTPPASSWORD: {0}'.format(SMTPSSL))


#SQLALCHEMY DATABASE URI: MySQL and SQLITE have been tested. Others should work.
#mysql+pymysql://<username>:<password>@<host>/<dbname>[?<options>]
DATABASEURI = os.getenv('DATABASEURI', 'sqlite:///cwd.db')
logging.error('DATABASEURI: {0}'.format(DATABASEURI))

#SUPER SECRET ACCESS KEY
#MUST MATCH THE KEY in cwd_status push.
API_KEY=os.getenv('API_KEY', 'YOURSECRETKEY')
logging.error('API_KEY: {0}'.format(API_KEY))

#GUI USER/PASSWORD
ADMINUSER=os.getenv('ADMINUSER', 'admin')
logging.error('ADMINUSER: {0}'.format(ADMINUSER))

ADMINPASS=os.getenv('ADMINPASS', 'changeme')
logging.error('ADMINPASS: {0}'.format(ADMINPASS))
