"""Run a number of processes which'll be proxied to by
NGINX
"""

import sys 
import os

if len(sys.argv) < 2:
    print "You must specify stop/start/restart"
    sys.exit(0)

cmd = sys.argv[-1]

http_port=5000
for s in ['first','second','third','fourth']:
    os.popen('/home/famoso_reports/Envs/famoso_reports/bin/pserve " \
            "--daemon --pid-file=/home/famoso_reports/famoso_reports/%s.pid "\
            "/home/famoso_reports/famoso_reports/production.ini " \
            "--log-file=/home/famoso_reports/famoso_reports/pyramid.log %s http_port=%s' % (s,cmd,http_port))
    http_port = http_port + 1
