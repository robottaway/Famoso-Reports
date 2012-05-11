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

@view_config(route_name='signin', renderer='signin.mak', permission='read')
def signin(request):
    if request.user:
        return HTTPFound(location=request.route_path('home'))
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
        request.session.flash("Your username or password is incorrect")
        return HTTPFound(location=request.route_path('signin'))
    request.session['userid'] = user.id
    return HTTPFound(location=request.route_path('home'))

@view_config(route_name='deauth', renderer=None)
def deauth(request):
    del request.session['userid']
    return HTTPFound(location=request.route_path('home'))

@view_config(route_name='user', renderer='user.mak', permission='read')
def user(context, request):
    if context is None:
        return HTTPNotFound
    if request.user.admin:
        groups = DBSession.query(ReportGroup).all()
    else:
        groups = []
    return {'user':context,'groups':groups}

@view_config(route_name='home', renderer='home.mak', permission='read')
def home(context, request):
    return {}

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

@view_config(route_name='update_user_groups', renderer=None, permission='write')
def update_user_groups(request):
    return HTTPFound(location=request.route_path('user'))

@view_config(route_name='emailtest', renderer='string')
def emailtest(request):
    mailer = get_mailer(request)
    message = Message(subject='famoso test', sender='robottaway@localhost',
                    recipients=['robottaway@gmail.com'],
                    body='Hi this is a test')
    mailer.send(message)
    return 'yup'

