import os
import traceback
import csv
import sys
import transaction

from sqlalchemy import engine_from_config

from pyramid_mailer.mailer import Mailer
from pyramid_mailer.message import Message

from pyramid.request import Request

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    bootstrap,
    )

from pyramid.renderers import render

from ..models import (
    DBSession,
    ReportGroup,
    Report,
    User,
    )

# Glabals for tracking events
new_groups = []
csv_files_missing_pdf = []
groups_new_reports = {}
user_new_reports = {}

def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd)) 
    sys.exit(1)


def handleReportFolder(reportFolder, report_group):
    """Crawl report group folder and find new reports"""

    global groups_new_reports, user_new_reports, csv_files_missing_pdf
    for root, subFolders, files in os.walk(reportFolder):
        for file in files:
            name, extension = os.path.splitext(file)
            
            if not extension:
                continue

            report = report_group.findReportNamed(name)
            if not report:
                report = Report()
                report.name = unicode(name)
                report.report_group = report_group
                DBSession.add(report)
                groups_new_reports.setdefault(report_group, []).append(report)
                for user in report_group.findAllUsers():
                    user_new_reports.setdefault(user, []).append(report)

            report.add_report_type(extension)


def handleRootFolder(rootFolder):
    global new_groups
    for root, subFolders, files in os.walk(rootFolder):
        for folder in subFolders:
            report_group = DBSession.query(ReportGroup).filter_by(name=unicode(folder)).first()
            if report_group is None:
                report_group = ReportGroup(name=unicode(folder))
                new_groups.append(report_group)
                DBSession.add(report_group)
            reportFolder = os.path.join(root, folder)
            handleReportFolder(reportFolder, report_group)


def email_users(request, mailer):
    """Send each user with new reports an email
    Don't email admins as we handle them separate. 
    """
    global user_new_reports

    for user in user_new_reports.keys():
        if user.admin:
            continue
        body = render('mail/newreports.mak', 
                {'user':user, 'user_new_reports':user_new_reports}, 
                request)
        message = Message(subject='Famoso Reports - New Reports', 
                    sender='Famoso Admin <admin@famosonut.com>',
                    recipients=[user.email],
                    body=body)
        mailer.send(message)


def email_admin_users(request, mailer):
    """Email admins, new reports, new groups, groups with
    new reports should be reported. Also report any funny
    business like csv files w/o a pdf.
    """
    global user_new_reports, groups_new_reports, new_groups, csv_files_missing_pdf

    admins = DBSession.query(User).filter_by(admin=True).all()
    for admin in admins:
        new_reports = user_new_reports.get(admin, None)
        if not new_reports:
            continue
        body = render('mail/adminstatusreport.mak', {
                 'user':admin,'new_reports':new_reports, 'new_groups':new_groups,
                 'csv_files_missing_pdf':csv_files_missing_pdf}, 
                 request)
        message = Message(subject='Famoso Reports - Status Report', 
                    sender='Famoso Admin <admin@famosonut.com>',
                    recipients=[admin.email],
                    body=body)
        mailer.send(message)


def main(argv=sys.argv):
    if len(argv) != 2:
        usage(argv)
    config_uri = argv[1]
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)
    engine = engine_from_config(settings, 'sqlalchemy.')
    mailer = Mailer.from_settings(settings)
    DBSession.configure(bind=engine)

    rootFolder = settings['reports.folder']

    request = Request.blank('/', base_url=settings['reports.app.url'])
    env = bootstrap(config_uri, request=request)
    request = env['request']

    try:
        handleRootFolder(rootFolder)
        email_users(request, mailer)
        email_admin_users(request, mailer)
        transaction.commit()
    except Exception as e:
        transaction.abort()
        stack = traceback.format_exc()
        print stack
        body = "Got an exception while processing reports: %s\n\n%s" % (e, stack)
        message = Message(subject='Famoso Reports - failed to process', 
                    sender='admin@famosonut.com',
                    recipients=['robottaway@gmail.com'],
                    body=body)
#        mailer.send_immediately(message)
	
