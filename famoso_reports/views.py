import re
import os

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound, HTTPNotFound, HTTPForbidden
from pyramid.renderers import render
from pyramid.response import FileResponse

from sqlalchemy.exc import DBAPIError

from pyramid_mailer import get_mailer
from pyramid_mailer.message import (
        Message,
        Attachment,
        )

from .models import (
    DBSession,
    User,
    ReportGroup,
    PASSWORD_MIN_LENGTH,
    USERNAME_MIN_LENGTH,
    EMAIL_REGEX,
    )

def forbidden(request):
    """If no user send them to log in, otherwise
    just re-raise the exception
    """
    if not request.user:
        return HTTPFound(location=request.route_path('signin'))
    raise request.exception

@view_config(route_name='home', renderer='signin.mak', permission='read')
@view_config(route_name='signin', renderer='signin.mak', permission='read')
def signin(request):
    if request.user:
        return HTTPFound(location=request.route_path('reportgroups'))
    return {}

@view_config(route_name='auth', renderer=None, permission='read')
def auth(request):
    username = request.params.get('username', None)
    password = request.params.get('password', None)
    if not username or not password:
        request.session.flash('Please enter username and password')
        return HTTPFound(location=request.route_path('signin'))
    try:
        user = DBSession.query(User).filter(User.username==username).first()
    except DBAPIError:
        request.session.flash('Authentication error, please contact support.')
        return HTTPFound(location=request.route_path('signin'))
    if not user or not user.verify(password):
        request.session.flash("Your username and/or password is incorrect")
        return HTTPFound(location=request.route_path('signin'))
    request.session['userid'] = user.id
    return HTTPFound(location=request.route_path('home'))

@view_config(route_name='deauth', renderer=None)
def deauth(request):
    if 'userid' in request.session:
        del request.session['userid']
    request.session.flash('You have been signed out')
    return HTTPFound(location=request.route_path('home'))

@view_config(route_name='user', renderer='user.mak', permission='read')
def user(user, request):
    if user is None:
        return HTTPNotFound()
    if request.user.admin:
        groups = DBSession.query(ReportGroup).all()
    else:
        groups = []
    return {'user':user,'groups':groups}

@view_config(route_name='update_password', renderer=None, permission='update')
def update_password(user, request):
    password = request.params.get('password', '')
    confirmpassword = request.params.get('confirmpassword', '')
    if '' in [password, confirmpassword]:
        request.session.flash('You must enter both values to change passwords')
    elif password == confirmpassword:
        if len(password) < PASSWORD_MIN_LENGTH:
            request.session.flash('Password must be 5 or more characters')
        else:    
            user.update_password(password)
            request.session.flash('Password Updated')
    else:
        request.session.flash('You need to enter matching values for the password')
    return HTTPFound(location=request.route_path('user', username=user.username))

@view_config(route_name='update_user_details', renderer=None, permission='update')
def update_user_details(user, request):
    first_name = request.params.get('first_name', '')
    last_name = request.params.get('last_name', '')
    email = request.params.get('email', '')
    if first_name != '' and user.first_name != first_name:
        request.session.flash('First name updated to %s' % first_name)
        user.first_name = first_name
    if last_name != '' and user.last_name != last_name:
        request.session.flash('Last name updated to %s' % last_name)
        user.last_name = last_name
    if email != '' and user.email != email:
        if not re.match(EMAIL_REGEX, email):
            request.session.flash('Not a valid email')
        else:
            request.session.flash('Email updated to %s' % email)
            user.email = email
    return HTTPFound(location=request.route_path('user', username=user.username))

@view_config(route_name='reportgroups', renderer='reportgroups.mak', permission='read')
def reportgroups(user, request):
    if not request.user:
	return HTTPForbidden('You must be signed in to access this resource')
    groups = request.user.findReportGroups()
    if len(groups) == 1:
        return HTTPFound(location=request.route_path('reportgroup', name=groups[0].name))
    return {'reportgroups': groups}

@view_config(route_name='reportgroup', renderer='reportgroup.mak', permission='read')
def reportgroup(reportgroup, request):
    cropyear = request.params.get('CropYear', None)
    reporttype = request.params.get('ReportGroup', None)
    reports = reportgroup.reports
    fatts = reportgroup.filterable_attributes()
    if cropyear:
        del fatts['CropYear'] 
        filtered = []
        for report in reports:
            if report.has_att_with_value('CropYear', cropyear):
                filtered.append(report)
        reports = filtered

    if reporttype:
        del fatts['ReportGroup'] 
        filtered = []
        for report in reports:
            if report.has_att_with_value('ReportGroup', reporttype):
                filtered.append(report)
        reports = filtered

    return {'reportgroup':reportgroup, 'reports':reports, 'fatts':fatts}

@view_config(route_name='report', renderer='report.mak', permission='read')
def report(reportgroup, request):
    reportname = request.matchdict.get('reportname', None)
    report = reportgroup.findReportNamed(reportname)
    if not report:
        return HTTPNotFound()
    return {'reportgroup':reportgroup, 'report': report}

@view_config(route_name='report_download', renderer=None, permission='read')
def report_download(reportgroup, request):
    f = request.matchdict.get('file', None)
    reportname = request.matchdict.get('reportname', None)
    reportgroup.findReportNamed(reportname)
    root = reportgroup.file_location(request)
    loc = "%s/%s" % (root, f)
    if not os.path.exists(loc):
        return HTTPNotFound()
    return FileResponse(loc, request)

#
# ADMIN VIEWS
#

@view_config(route_name="admin", renderer='admin.mak', permission='read')
def admin(request):
    users = DBSession.query(User).all()
    groups = DBSession.query(ReportGroup).all()
    return {'users':users,'groups':groups}


@view_config(route_name='new_user', renderer='create_user.mak', permission='read')
def new_user(request):
    return {}

@view_config(route_name="rename_reportgroup", renderer=None, permission='create')
def rename_reportgroup(reportgroup, request):
    name = request.params.get('newname', None)
    if not name:
        request.session.flash('You must include a new name')
    elif len(name) > 256:
        request.session.flash('New name can have a maximum of 256 characters')
    else:
	if reportgroup.displayname != name:
            reportgroup.displayname = name
            request.session.flash('Name updated')
        else:
            request.session.flash('Name not changed')
    return HTTPFound(location=request.route_path('reportgroup', name=reportgroup.name))

@view_config(route_name='create_user', renderer=None, permission='create')
def create_user(request):
    username = request.params.get('username', None)
    if not username:
        request.session.flash('You must include a username')
    if len(username) < USERNAME_MIN_LENGTH:
        request.session.flash('Username must be at least %s characters' % USERNAME_MIN_LENGTH)
    if DBSession.query(User).filter_by(username=username).first():
        request.session.flash('Username is already taken')
    password = request.params.get('password', None)
    if not password:
        request.session.flash('You must include a password')
    if len(password) < PASSWORD_MIN_LENGTH:
        request.session.flash('Password must be at least %s characters long' % PASSWORD_MIN_LENGTH)
    confirmpassword = request.params.get('confirmpassword', None)
    if not confirmpassword:
        request.session.flash('You must confirm the password')
    if password != confirmpassword:    
        request.session.flash('Passwords do not match')
    first_name = request.params.get('first_name', None)
    if not first_name:
        request.session.flash('You must include a first name')
    last_name = request.params.get('last_name', None)
    if not last_name:
        request.session.flash('You must include a last name')
    email = request.params.get('email', None)
    if not email:
        request.session.flash('You must include an email')
    if DBSession.query(User).filter(User.email == email).count():
        request.session.flash("The email '%s' is already in use by another account" % email)
    admin = True if request.params.get('admin', None) else False
    if not request.session.peek_flash():
        user = User(username, password, email, admin, first_name, last_name)
        request.session.flash('User created')
        DBSession.add(user)
        mailer = get_mailer(request)
        body = render('mail/newuser.mak', {'user':user}, request)
        message = Message(subject='Famoso Reporting - New Account for %s' % user.displayName(), 
                    sender='Famoso Admin <admin@famosonut.com>',
                    recipients=[user.email],
                    body=body)
        mailer.send(message)
        return HTTPFound(location=request.route_path('user', username=username))
    return HTTPFound(location=request.route_path('new_user'))


@view_config(route_name='update_user_groups', renderer=None, permission='update_groups')
def update_user_groups(user, request):
    groups = request.params.getall('groups')
    all_groups = []
    new_groups = []
    gone_groups = []
    for group in groups:
        group = DBSession.query(ReportGroup).filter_by(name=group).first()
        if group: 
            all_groups.append(group)
            if group not in user.report_groups:
                new_groups.append(group)
                request.session.flash('Added to group %s' % group.name)
    for group in user.report_groups:
        if not group in all_groups:
            gone_groups.append(group)
            request.session.flash('Removed from group %s' % group.name)
    user.report_groups = all_groups
    mailer = get_mailer(request)
    body = render('mail/newgroups.mak', 
                {'user':user,'new_groups':new_groups,'gone_groups':gone_groups}, 
                request)
    message = Message(subject='New Reports Available', 
                sender='Famoso Admin <admin@famosonut.com>',
                recipients=[user.email],
                body=body)
    mailer.send(message)
    return HTTPFound(location=request.route_path('user', username=user.username))


def email_to(request, usernames, report):
    """Send the csv and pdf file for report to given users"""

    mailer = get_mailer(request)
    files = report.file_locations(request)
    attachments = []
    for location, filename, extension, mime in files:
        attachment = Attachment(filename, mime, open(location, "rb"), 'attachment')
        attachments.append(attachment)

    for username in usernames:
        user = DBSession.query(User).filter_by(username=username).first()
        if not user:
            continue
        body = render('mail/report.mak', {'user':user, 'report':report}, request)
        message = Message(subject='Famoso Reporting - %s' % report.name,
                    sender='Famoso Admin <admin@famosonut.com>',
                    recipients=[user.email],
                    body=body,
                    attachments=attachments)
        mailer.send_immediately(message)


@view_config(route_name='email_report', renderer=None, permission='email')
def email_report(reportgroup, request):
    reportname = request.matchdict.get('reportname', None)
    report = reportgroup.findReportNamed(reportname)
    mailto = request.params.getall('mailto')
    email_to(request, mailto, report)
    request.session.flash('Email Sent')
    return HTTPFound(location=request.route_path('report', name=reportgroup.name, reportname=report.name))


@view_config(route_name='error', renderer=None)
def error(request):
    """To Test email of exceptions works"""
    raise Exception('blah')
