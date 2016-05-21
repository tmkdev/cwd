#!/usr/bin/env bash
#
#cwd_statusurl can either be set global or passed.. ie:
#cwd_statusurl="http://yourinstance" ./cwd_status.sh jobname start/end/fail
#Or you can implement a HTTP get with your language/command of choice.
API_KEY="YOURSECRETKEY"

jobname=$1
status=$2

url="${cwd_statusurl}/status/${jobname}/${status}"

curl --connect-timeout 2 --max-time 4 --data "cwd_apikey=${API_KEY}" -s -k ${url} > /dev/null
