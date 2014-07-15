famoso_reports README
==================

Getting Started
---------------

As a prerequiste you'll need virtualenv and virtualenvwrapper installed.

- cd <directory containing this file>

- mkvirtualenv famoso_reports

- python setup.py develop

- pserve development.ini

- initialize_db development.ini

- update_user development.ini root <new password>


As another strategy for setting up the database you could run the numbered sql files in the sql folder.


Psycopg
---------------------------------------
OS X macports add pg_conf location such as:

/opt/local/lib/postgresql91/bin/

To path before pip install to make sure psycopg installs.

With Homebrew install of Postgres no change was needed to install the driver.


Cron Jobs
--------------------------------------
You will need to setup synching files from the REACTS export folder:

MAILTO=robottaway@gmail.com
# m h  dom mon dow   command
*/5 * * * * rsync -rz -e ssh server2:/cygdrive/d/REACTS/Export/* /var/reports/; find /var/reports -type d -exec chmod 755 {} \;; find /var/reports -type f -exec chmod 644 {} \;;

The above is an example of synching the folders and files from the one server 
to the other and then also making sure file permissions on those files are 
usable.

For the script named 'process_new_reports' you will want to schedule a run of
the script at least once a day. You should schedule this to run after the rsync
process has completed adding or deleting any new exported files from the REACTS
server.

MAILTO=robottaway@gmail.com
# m h  dom mon dow   command
45 8,10,12,14,16 * * * /home/famoso_reports/Envs/famoso_reports/bin/process_new_reports famoso_reports/production.ini

