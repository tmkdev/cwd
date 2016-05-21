CWD - Cron Watch Dog

tmkdev llc - 2016

I needed a simple web service to monitor small applications that are dependant on cron jobs running.

I found some SaaS solutions - none of them were exactly what I was looking for.
(https://steward.io/, https://deadmanssnitch.com/, webcron.com)

So I wrote this.

Released as https://opensource.org/licenses/GPL-2.0  - GPL-2.0 opensource.

Setup:

Install the python requirements:
    sqlalchemy
    bottle
    bottle-sqlalchemy
    db driver of choice (Mysql and sqlite tested)


1. Copy configuration_dist.py to configuration.py. Edit with your values.
2. Add to apache. Or run as a stand alone service using Bottle.py's built in service. Or your favorite WSGI server.
    - if you use app.py and bottle's built in wsgi, it will start a thread for cwd_checker. Ignore 3.
3. Set the job monitor service to run.

    CRONENTRY
    @reboot /usr/bin/python cwd_checker.py > logfile.log 2>&1;

3. Log in. Bottle starts service at 8080. Your apache conf should start it where you tell it.
4. Set up cwd_status.sh to run before and after your monitored jobs. Set up the URL vars as needed.
    cwd_status.sh jobnametomonitor start\
    jobname && cwd_status.sh jobnametomonitor end \
            || cwd_status.sh jobnametomonitor fail
5. Edit the periodicity of your job and SLA levels in the GUI.


Apache sample site conf (Needs Mod-wsgi)
<Virtualhost *:80>

	    WSGIPassAuthorization on
      	WSGIDaemonProcess cwd user=www-data group=www-data processes=1 threads=5
        WSGIScriptAlias /cwd /home/ubuntu/cwd/app.wsgi

    	<Directory /home/ubuntu/cwd>
        	WSGIProcessGroup cwd
        	WSGIApplicationGroup %{GLOBAL}
		    Require all granted
        	Order deny,allow
    	</Directory>

</Virtualhost>
