from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound, HTTPNotFound

from sqlalchemy.exc import DBAPIError

from pyramid_mailer import get_mailer
from pyramid_mailer.message import Message

from .models import (
    DBSession,
    User,
    ReportGroup,
    )

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
        if len(password) < 5:
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
        request.session.flash('Email updated to %s' % email)
        user.email = email
    return HTTPFound(location=request.route_path('user', username=user.username))

@view_config(route_name='reportgroups', renderer='reportgroups.mak', permission='read')
def reportgroups(request):
    groups = request.user.findReportGroups()
    if len(groups) == 1:
        return HTTPFound(location=request.route_path('reportgroup', name=groups[0].name))
    return {'reportgroups': groups}

@view_config(route_name='reportgroup', renderer='reportgroup.mak', permission='read')
def reportgroup(context, request):
    return {'reportgroup':context}

@view_config(route_name='report', renderer='report.mak', permission='read')
def report(context, request):
    reportname = request.matchdict.get('reportname', None)
    report = context.findReportNamed(reportname)
    return {'reportgroup':context, 'report': report}

#
# ADMIN VIEWS
#

@view_config(route_name="admin", renderer='admin.mak', permission='read')
def admin(request):
    users = DBSession.query(User).all()
    groups = DBSession.query(ReportGroup).all()
    return {'users':users,'groups':groups}

@view_config(route_name='create_user', renderer='create_user.mak', permission='read')
def create_user(request):
    return {}

@view_config(route_name='update_user_groups', renderer=None, permission='update_groups')
def update_user_groups(user, request):
    groups = request.params.getall('groups')
    new_groups = []
    remove_groups = []
    for group in groups:
        group = DBSession.query(ReportGroup).filter_by(name=group).first()
        if group: 
            new_groups.append(group)
            if group not in user.report_groups:
                request.session.flash('Added to group %s' % group.name)
    for group in user.report_groups:
        if not group in new_groups:
            request.session.flash('Removed from group %s' % group.name)
    user.report_groups = new_groups
    return HTTPFound(location=request.route_path('user', username=user.username))

@view_config(route_name='emailtest', renderer='string')
def emailtest(request):
    mailer = get_mailer(request)
    message = Message(subject='famoso test', sender='robottaway@localhost',
                    recipients=['robottaway@gmail.com'],
                    body='Hi this is a test')
    mailer.send(message)
    return 'yup'

