#EMAIL SERVER SETTINGS
CWDPAGEEMAIL = 'cronwatchdog@yourdomain.com'  #CWD SEND email address
CWDDOMAIN = 'yourdomain.com'          #SMTP SSL DOMAIN.
SMTPSERVER = 'yoursmtpserver.com'     #SMTP SERVER
SMTPUSER = 'yoursmtpuser'             #SMTP User if authentication/SSL is needed
SMTPPORT = '123'                      #SMTP Port
SMTPPASSWORD = 'yourpassword'         #SMTP Authentication
SMTPSSL = True                        #SMTP Uses SSL and authenticates?

#SQLALCHEMY DATABASE URI: MySQL and SQLITE have been tested. Others should work.
DATABASEURI = 'sqlite:///cwd.db'

#SUPER SECRET ACCESS KEY
#MUST MATCH THE KEY in cwd_status push.
API_KEY='YOURSECRETKEY'

#GUI USER/PASSWORD
ADMINUSER='admin'
ADMINPASS='changeme'