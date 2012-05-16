from pyramid_beaker import session_factory_from_settings
from pyramid.config import Configurator
from pyramid.authorization import ACLAuthorizationPolicy

from sqlalchemy import engine_from_config

from .models import (
    DBSession,
    User,
    Root,
    Admin,
    UserFactory,
    ReportGroupFactory,
    )
from famoso_reports.security import FamosoAuthenticationPolicy

def get_user(request):
    # the below line is just an example, use your own method of
    # accessing a database connection here (this could even be another
    # request property such as request.db, implemented using this same
    # pattern).
    userid = request.session.get('userid', None)
    if userid is not None:
        # this should return None if the user doesn't exist
        # in the database
        return DBSession.query(User).get(userid)
    return None

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    config = Configurator(
                root_factory=Root,
                settings=settings,
                authentication_policy=FamosoAuthenticationPolicy(),
                authorization_policy=ACLAuthorizationPolicy(),
    )

    session_factory = session_factory_from_settings(settings)
    config.set_session_factory(session_factory)

    config.set_request_property(get_user, 'user', reify=True)

    config.add_static_view('static', 'static', cache_max_age=3600)

    add_routes(config)

    config.scan('famoso_reports.views')
    return config.make_wsgi_app()


def add_routes(config):
    """Add all the routes given the config"""

    config.add_route('home', '/', request_method='GET') # same view as signin
    config.add_route('signin', '/signin', request_method='GET')
    config.add_route('auth', '/auth', request_method='POST')
    config.add_route('deauth', '/deauth', request_method='GET')
    config.add_route('user', '/user/{username}', request_method='GET',
            factory=UserFactory)
    config.add_route('update_password', '/user/{username}/password', 
            factory=UserFactory, request_method='POST')
    config.add_route('update_user_details', '/user/{username}/details', 
            factory=UserFactory, request_method='POST')
    config.add_route('update_user_groups', '/user/{username}/update_user_groups', 
            request_method='POST', factory=UserFactory)
    config.add_route('reportgroups', '/reportgroup', request_method='GET')
    config.add_route('reportgroup', '/reportgroup/{name}', request_method='GET',
            factory=ReportGroupFactory)
    config.add_route('report', '/reportgroup/{name}/report/{reportname}', 
            request_method='GET', factory=ReportGroupFactory)
    config.add_route('email_report', '/reportgroup/{name}/report/{reportname}/email',
            request_method='POST', factory=ReportGroupFactory)
    config.add_route('admin', '/admin', factory=Admin, request_method='GET')
    config.add_route('new_user', '/admin/new_user', factory=Admin, request_method='GET')
    config.add_route('create_user', '/admin/create_user', factory=Admin, request_method='POST')

