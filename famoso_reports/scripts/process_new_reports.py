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


def handleMetadata(request, report_group, report):
    location = report.file_location_for_type(request, '.meta')
    fd = open(location, 'r')
    csvr = csv.reader(fd, delimiter=',')
    colnames = csvr.next()
    values = csvr.next()
    d = dict(zip(colnames, values))
    for k, v in d.items():
        report.add_or_update_attribute(k, v)


def handleReportFolder(request, reportFolder, report_group):
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
                report.displayname = unicode(name)
                report.report_group = report_group
                report.add_report_type(extension)
                DBSession.add(report)

                groups_new_reports.setdefault(report_group, []).append(report)
                for user in report_group.findAllUsers():
                    user_new_reports.setdefault(user, []).append(report)
            else:
                report.add_report_type(extension)

            if extension == '.meta':
                handleMetadata(request, report_group, report)


def handleRootFolder(request, rootFolder):
    global new_groups

    for root, subFolders, files in os.walk(rootFolder):
        for folder in subFolders:
            report_group = DBSession.query(ReportGroup).filter_by(name=unicode(folder)).first()
            if report_group is None:
                report_group = ReportGroup(name=unicode(folder))
                new_groups.append(report_group)
                DBSession.add(report_group)
            reportFolder = os.path.join(root, folder)
            handleReportFolder(request, reportFolder, report_group)


def email_users(request, mailer):
    """Send each user with new reports an email
    Don't email admins as we handle them separate. 
    """
    global user_new_reports

    for user in user_new_reports.keys():
        if user.admin:
            continue
        new_reports = user_new_reports.get(user, None)
        if not new_reports:
            continue
        body = render('mail/newreports.mak', 
                {'user':user, 'new_reports':new_reports}, 
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


def remove_groups(request):
    groups = DBSession.query(ReportGroup).all() 
    for group in groups:
        loc = group.file_location(request)
        if not os.path.exists(loc):
            print "Deleting group %s" % group.name
            DBSession.delete(group)


def remove_reports(request):
    reports = DBSession.query(Report).all()
    for report in reports:
        has_any = False
        for loc, _, _, _ in report.file_locations(request):
            if os.path.exists(loc):
                has_any = True
                break
        if not has_any:
            DBSession.delete(report)


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
        remove_groups(request)
        remove_reports(request)
        handleRootFolder(request, rootFolder)
        email_users(request, mailer)
        email_admin_users(request, mailer)
        transaction.commit()
    except Exception as e:
        transaction.abort()
        stack = traceback.format_exc()
        body = "Got an exception while processing reports: %s\n\n%s" % (e, stack)
        message = Message(subject='Famoso Reports - failed to process', 
                    sender='admin@famosonut.com',
                    recipients=['robottaway@gmail.com'],
                    body=body)
        mailer.send_immediately(message)
	
