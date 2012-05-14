from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.renderers import render

from sqlalchemy.exc import DBAPIError

from pyramid_mailer import get_mailer
from pyramid_mailer.message import Message

import transaction

from .models import (
    DBSession,
    User,
    ReportGroup,
    PASSWORD_MIN_LENGTH,
    USERNAME_MIN_LENGTH,
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

@view_config(route_name='new_user', renderer='create_user.mak', permission='read')
def new_user(request):
    return {}

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
    admin = True if request.params.get('admin', None) else False
    if not request.session.peek_flash():
        user = User(username, password, email, admin, first_name, last_name)
        request.session.flash('User created')
        DBSession.add(user)
        mailer = get_mailer(request)
        body = render('mail/newuser.mak', {'user':user}, request)
        message = Message(subject='Famoso Reporting Account for %s' % user.displayName(), 
                    sender='admin@famosonut.com',
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
                sender='admin@famosonut.com',
                recipients=[user.email],
                body=body)
    mailer.send(message)
    return HTTPFound(location=request.route_path('user', username=user.username))

