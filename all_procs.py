import sys 
import os

if len(sys.argv) < 2:
    print "You must specify stop/start/restart"
    sys.exit(0)

cmd = sys.argv[-1]

http_port=5000
for s in ['first','second','third','fourth']:
    os.popen('pserve --daemon --pid-file=%s.pid production.ini %s http_port=%s' % (s,cmd,http_port))
    http_port = http_port + 1
