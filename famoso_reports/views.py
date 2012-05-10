from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from sqlalchemy.exc import DBAPIError

from pyramid_mailer import get_mailer
from pyramid_mailer.message import Message

from .models import (
    DBSession,
    User,
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
        print "no user found"
    return {}

@view_config(route_name='home', renderer='test.mak', permission='read')
def home(context, request):
    print request.user
    return {}

@view_config(route_name='reportgroup', renderer='reportgroup.mak', permission='read')
def reportgroup(context, request):
    return {'reportgroup':context}

@view_config(route_name='emailtest', renderer='string')
def emailtest(request):
    mailer = get_mailer(request)
    message = Message(subject='famoso test', sender='robottaway@localhost',
                    recipients=['robottaway@gmail.com'],
                    body='Hi this is a test')
    mailer.send(message)
    return 'yup'

