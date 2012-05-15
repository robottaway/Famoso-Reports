import os
import csv
import sys
import transaction

from sqlalchemy import engine_from_config

from pyramid_mailer.mailer import Mailer
from pyramid_mailer.message import Message

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from ..models import (
    DBSession,
    ReportGroup,
    Report
    )

new_groups = []
groups_new_reports = {}
user_new_reports = {}

def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd)) 
    sys.exit(1)

def reportFromRow(row):
    report = Report()
    report.usdaid = unicode(row[0])
    report.grower = unicode(row[1])
    report.block = unicode(row[2])
    report.variety = unicode(row[3])
    report.county = unicode(row[4])
    report.lot = unicode(row[5])
    report.commodity = unicode(row[6])
    report.handler = unicode(row[7])
    report.certificate = unicode(row[8])
    report.date_certified = unicode(row[9])
    report.gross_weight = int(row[10])
    report.edible_kernal_weight = int(row[11])
    report.inedible_kernal_weight = int(row[12])
    report.foreign_material_weight = int(row[13])
    report.shell_out_loss = int(row[14])
    report.excess_moisture = int(row[15])
    report.crop_year = int(row[16])
    report.acres = int(row[17])
    return report


def handleReportFolder(reportFolder, report_group):
    global groups_new_reports, user_new_reports
    for root, subFolders, files in os.walk(reportFolder):
        for file in files:
            name, extension = os.path.splitext(file)
            if extension == '.csv':
                pdf_file_name = ''.join([name, '.pdf'])
                if not os.path.exists(os.path.join(root, pdf_file_name)):
                    print "Matching pdf file does not exist for csv file '%s'" % file
                    continue
                report = report_group.findReportNamed(name)
                if not report:
                    full_path = os.path.join(root, file)
                    print "found file: '%s'" % full_path
                    csvreader = csv.reader(open(full_path, 'rb'), delimiter=',', quotechar='\'')
                    csvreader.next() # burn the header
                    values = csvreader.next()
                    report = reportFromRow(values)
                    report.name = unicode(name)
                    report.report_group = report_group
                    DBSession.add(report)
                    groups_with_new_reports.add(report_group)
		    for user in report_group.users:
		        user_new_reports.setdefault(user.username], []).append(link)
    print ''


def handleRootFolder(rootFolder):
    global new_groups
    for root, subFolders, files in os.walk(rootFolder):
        for folder in subFolders:
            print "Report Group Folder '%s'\n----------------------" % folder
            report_group = DBSession.query(ReportGroup).filter_by(name=unicode(folder)).first()
            if report_group is None:
                report_group = ReportGroup(name=unicode(folder))
                new_groups.append(report_group)
                DBSession.add(report_group)
            reportFolder = os.path.join(root, folder)
            handleReportFolder(reportFolder, report_group)

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

    print "Processing reports in folder '%s'" % rootFolder
    try:
        handleRootFolder(rootFolder)
    except Exception as e:
	transaction.abort()
	print "Got an exception while processing reports: %s" % e
	body = str(e)
        message = Message(subject='Famoso Reports - failed to process', 
                    sender='admin@famosonut.com',
                    recipients=['robottaway@gmail.com'],
                    body=body)
        mailer.send(message)
	
