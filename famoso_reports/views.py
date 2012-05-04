from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from pyramid_mailer import get_mailer
from pyramid_mailer.message import Message

from .models import (
    DBSession,
    MyModel,
    )

@view_config(route_name='signin', renderer='signin.mak')
def signin(request):
    return {}

@view_config(route_name='home', renderer='test.mak')
def my_view(request):
    request.session['abc'] = 'hi'
    try:
        one = DBSession.query(MyModel).filter(MyModel.name=='one').first()
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return {'one':one, 'project':'famoso_reports'}

@view_config(route_name='emailtest', renderer='string')
def emailtest(request):
    mailer = get_mailer(request)
    message = Message(subject='famoso test', sender='robottaway@localhost',
                    recipients=['robottaway@gmail.com'],
                    body='Hi this is a test')
    mailer.send(message)
    return 'yup'

conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_famoso_reports_db" script
    to initialize your database tables.  Check your virtual 
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""

