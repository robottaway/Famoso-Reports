import os
import sha

from pyramid.security import Allow
from pyramid.security import Everyone
from pyramid.httpexceptions import HTTPNotFound, HTTPInternalServerError

from sqlalchemy import (
    Column,
    Integer,
    String,
    Unicode,
    Boolean,
    Table,
    ForeignKey,
    )
from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    relationship,
    backref,
    )
from sqlalchemy.schema import UniqueConstraint

from zope.sqlalchemy import ZopeTransactionExtension

class Root(object):
    """Root context has no acl"""

    __acl__ = []
    
    def __init__(self, request):
        self.__acl__ = [
            (Allow, Everyone, 'read'), # Let everyone view default resources
            (Allow, 'admin', 'create'),
            (Allow, 'admin', 'read'),
            (Allow, 'admin', 'update'),
            (Allow, 'admin', 'delete'),
        ]

class Admin(object):

    __acl__ = []

    def __init__(self, request):
        self.__acl__ = [
            (Allow, 'admin', 'create'),
            (Allow, 'admin', 'read'),
            (Allow, 'admin', 'update'),
            (Allow, 'admin', 'delete'),
        ]


DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

class UserNotFound(object):
    pass

PASSWORD_MIN_LENGTH = 5
USERNAME_MIN_LENGTH = 3
EMAIL_REGEX = "^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$"

class User(Base):
    __tablename__ = 'appusers'
    id = Column(Integer, primary_key=True)
    username = Column(Unicode(20), unique=True, nullable=False)
    password = Column(String(80), nullable=False)
    first_name = Column(Unicode(64), nullable=False)
    last_name = Column(Unicode(64), nullable=False)
    email = Column(Unicode(256), unique=True, nullable=False)
    admin = Column(Boolean, nullable=False, default=False)

    def __init__(self, username=None, password=None, email=None, admin=False,
            first_name=None, last_name=None):
        self.username = username
        self.email = email
        self.admin = admin
        self.first_name = first_name
        self.last_name = last_name
        if password:
            self.update_password(password)

    def displayName(self):
        return "%s %s" % (self.first_name, self.last_name)

    def update_password(self, password):
        self.password = self.crypt_password(password)

    def crypt_password(self, plaintext):
        if isinstance(plaintext, unicode):
            plaintext = plaintext.encode('utf-8')
        salt = sha.new(os.urandom(60)).hexdigest()
        cryptval = sha.new(plaintext + salt).hexdigest()
        return salt + cryptval

    def verify(self, plaintext):
        if isinstance(plaintext, unicode):
            plaintext = plaintext.encode('utf-8')
        password_salt = self.password[:40]
        plaintext = plaintext.encode('ascii', 'ignore')
        crypt_pass = sha.new(plaintext + password_salt).hexdigest()
        if crypt_pass == self.password[40:]:
            return True
        else:
            return False

    def findReportGroups(self):
        if self.admin:
            return DBSession.query(ReportGroup).all()
        return self.report_groups

    def hasReportGroup(self, tofind):
        for group in self.report_groups:
            if group.id == tofind.id:
                return True
        return False

    def __str__(self):
        return "<User username: '%s', email: '%s'>" % (self.username, self.email)

def UserFactory(request):
    """Provide the User model as context, or None if not found"""

    username = request.matchdict.get('username', None)
    try:
        user = DBSession.query(User).filter(User.username==username).first()
        if not user:
            raise HTTPNotFound
        user.__name__ = 'user'
        user.__parent__ = None
        user.__acl__ = [
            (Allow, 'admin', 'create'),
            (Allow, 'admin', 'read'),
            (Allow, 'admin', 'update'),
            (Allow, 'admin', 'delete'),
            (Allow, 'admin', 'update_groups'),
            (Allow, 'user:%s' % user.username, 'read'),
            (Allow, 'user:%s' % user.username, 'update'),
        ]
    except DBAPIError:
        return HTTPInternalServerError
    return user

report_group_users = Table('report_group_users', Base.metadata,
    Column('report_group_id', Integer, ForeignKey('reportgroups.id'), nullable=False),
    Column('user_id', Integer, ForeignKey('appusers.id'), nullable=False),
    UniqueConstraint('report_group_id', 'user_id', name='user_report_uc')
)

class ReportGroup(Base):
    __tablename__ = 'reportgroups'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(256), unique=True, nullable=False)
    displayname = Column(Unicode(256), unique=True, nullable=False)

    users = relationship('User', secondary=report_group_users, backref='report_groups')
    
    def __init__(self, name=None, displayname=None): 
        self.name = name
        self.displayname = displayname or name

    def findReportNamed(self, name):
        for report in self.reports:
            if report.name == name:
                return report
        return None

def ReportGroupFactory(request):
    name = request.matchdict.get('name', None)
    if not name:
        return None
    try:
        group = DBSession.query(ReportGroup).filter_by(name=name).first()
        if not group:
            return HTTPNotFound
        group.__name__ = 'reportgroup'
        group.__parent__ = None
        group.__acl__ = [
            (Allow, 'admin', 'create'),
            (Allow, 'admin', 'read'),
            (Allow, 'admin', 'update'),
            (Allow, 'admin', 'delete'),
            (Allow, 'reportgroup:%s' % group.name, 'read'),
        ] 
    except DBAPIError:
        return HTTPInternalServerError
    return group

class Report(Base):
    __tablename__ = 'report'
    __table_args__ = (
            UniqueConstraint('name', 'report_group_id', name='name_group_uc'),
    )

    id = Column(Integer, primary_key=True)
    name = Column(Unicode(256), nullable=False)
    report_group_id = Column(Integer, ForeignKey('reportgroups.id'), nullable=False)
    usdaid = Column(Unicode(256), nullable=False)
    grower = Column(Unicode(256), nullable=False)
    block = Column(Unicode(256), nullable=False)
    variety = Column(Unicode(256), nullable=False)
    county = Column(Unicode(256), nullable=False)
    lot = Column(Unicode(256), nullable=False)
    commodity = Column(Unicode(256), nullable=False)
    handler = Column(Unicode(256), nullable=False)
    certificate = Column(Unicode(256), nullable=False)
    date_certified = Column(Unicode(256), nullable=False)
    gross_weight = Column(Integer, nullable=False)
    edible_kernal_weight = Column(Integer, nullable=False)
    inedible_kernal_weight = Column(Integer, nullable=False)
    foreign_material_weight = Column(Integer, nullable=False)
    shell_out_loss = Column(Integer, nullable=False)
    excess_moisture = Column(Integer, nullable=False)
    crop_year = Column(Integer, nullable=False)
    acres = Column(Integer, nullable=False)

    report_group = relationship('ReportGroup', backref=backref('reports', order_by=id))

    def __init__(self):
        pass
