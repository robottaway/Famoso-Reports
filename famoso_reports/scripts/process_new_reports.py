import os
import csv
import sys
import transaction

from sqlalchemy import engine_from_config

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
groups_with_new_reports = []

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
    print ''


def handleRootFolder(rootFolder):
    for root, subFolders, files in os.walk(rootFolder):
        for folder in subFolders:
            print "Report Group Folder '%s'\n----------------------" % folder
            with transaction.manager:
                report_group = DBSession.query(ReportGroup).filter_by(name=unicode(folder)).first()
                if report_group is None:
            request.session.flash('Added to group %s' % group.name)
                    report_group = ReportGroup(name=unicode(folder))
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
    DBSession.configure(bind=engine)

    rootFolder = settings['reports.folder']

    print "Processing reports in folder '%s'" % rootFolder

    handleRootFolder(rootFolder)
