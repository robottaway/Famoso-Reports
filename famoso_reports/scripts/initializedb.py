import os
import sys
import transaction

from sqlalchemy import engine_from_config

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from ..models import (
    DBSession,
    User,
    Base,
    )

def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd)) 
    sys.exit(1)

def main(argv=sys.argv):
    if len(argv) != 2:
        usage(argv)
    config_uri = argv[1]
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    with transaction.manager:
        user = DBSession.query(User).filter_by(username=u'root').first()
        if not user:
            user = User(username=u'root', password=u'blahblah', 
                        email=u'robottaway+famosoroot@gmail.com', admin=True,
                        first_name=u'root', last_name=u'user')
            DBSession.add(user)
            user = User(username=u'testguy', password=u'password', 
                        email=u'robottaway+testguy@gmail.com', admin=False,
                        first_name=u'Test', last_name=u'Guy')
            DBSession.add(user)
