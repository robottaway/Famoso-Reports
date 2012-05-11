from pyramid_beaker import session_factory_from_settings
from pyramid.config import Configurator
from pyramid.authorization import ACLAuthorizationPolicy

from sqlalchemy import engine_from_config

from .models import (
    DBSession,
    User,
    Root,
    Admin,
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

    config.add_route('home', '/')
    config.add_route('emailtest', '/emailtest')
    config.add_route('signin', '/signin')
    config.add_route('auth', '/auth')
    config.add_route('deauth', '/deauth')
    config.add_route('user', '/user/{username}', factory='famoso_reports.models.UserFactory')
    config.add_route('reportgroups', '/reportgroup')
    config.add_route('reportgroup', '/reportgroup/{name}', factory='famoso_reports.models.ReportGroupFactory')
    config.add_route('report', '/reportgroup/{name}/report/{reportname}', factory='famoso_reports.models.ReportGroupFactory')
    config.add_route('admin', '/admin', factory=Admin)

    config.scan('famoso_reports.views')
    return config.make_wsgi_app()

