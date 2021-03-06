import os
import hashlib

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
        salt = hashlib.sha1(os.urandom(60)).hexdigest()
        cryptval = hashlib.sha1(plaintext + salt).hexdigest()
        return salt + cryptval

    def verify(self, plaintext):
        if isinstance(plaintext, unicode):
            plaintext = plaintext.encode('utf-8')
        password_salt = self.password[:40]
        plaintext = plaintext.encode('ascii', 'ignore')
        crypt_pass = hashlib.sha1(plaintext + password_salt).hexdigest()
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
    reports = relationship('Report', backref="report_group", cascade="all, delete, delete-orphan")
    
    def __init__(self, name=None, displayname=None): 
        self.name = name
        self.displayname = displayname or name

    def findReportNamed(self, name):
        for report in self.reports:
            if report.name == unicode(name):
                return report
        return None

    def findAllUsers(self):
        """Return users in this report group and admins,
        all users with access"""

        admins = DBSession.query(User).filter_by(admin=True).all()
        return set(self.users + admins)

    def file_location(self, request):
        root = request.registry.settings.get('reports.folder', '')
        group_loc = "%s/%s" % (root, self.name)
        return group_loc

    def filterable_attributes(self):
        atts = DBSession.query(ReportAttribute.name, ReportAttribute.value) \
            .outerjoin(Report, Report.id==ReportAttribute.report_id) \
            .outerjoin(ReportGroup, ReportGroup.id==Report.report_group_id) \
            .filter(ReportGroup.id==self.id) \
            .distinct().all()
        combined = {}
        for att in atts:
            combined.setdefault(att.name, []).append(att.value)
        for attrname in combined.keys():
            combined[attrname].sort()
        return combined

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
            (Allow, 'admin', 'email'),
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
    displayname = Column(Unicode(256), nullable=False)
    report_group_id = Column(Integer, ForeignKey('reportgroups.id'), nullable=False)

    attributes = relationship('ReportAttribute', backref='report', cascade='all, delete, delete-orphan')

    @property
    def file_names(self):
        names = []
        for report_type in self.report_types:
            names.append("%s%s" % (self.name, report_type.extension))
        return names

    def file_location_for_type(self, request, extension):
        root = self.report_group.file_location(request)
        for report_type in self.report_types:
            if report_type.extension == extension:
                return "%s/%s%s" % (root, self.name, report_type.extension)
        return None

    def file_locations(self, request):
        root = self.report_group.file_location(request)
        files = []
        for report_type in self.report_types:
            filename = "%s%s" % (self.name, report_type.extension)
            location = "%s/%s%s" % (root, self.name, report_type.extension)
            mime = self.mime_for_extension(report_type.extension)
            files.append((location, filename, report_type.extension, mime))
        return files

    def mime_for_extension(self, ext):
        if ext == 'csv':
            return 'text/csv'
        if ext == 'pdf':
            return 'application/pdf'
        return 'application/octet-stream'

    def add_report_type(self, extension):
        report_type = DBSession.query(ReportType).filter_by(extension=extension).first()
        if not report_type:
            report_type = ReportType(extension)
            DBSession.add(report_type)
        if report_type not in self.report_types:
            self.report_types.append(report_type)
        return report_type

    def add_or_update_attribute(self, name, value):
        if name == 'ReportName':
            self.displayname = unicode(value)
            return
        for att in self.attributes:
            if att.name == name:
                att.value = unicode(value)
                return
        att = ReportAttribute(name, value)
        self.attributes.append(att)

    def has_att_with_value(self, name, value):
        for att in self.attributes:
            if att.name == name and att.value == value:
                return True
        return False

    def __init__(self):
        pass

report_report_types = Table('report_report_type', Base.metadata,
    Column('report_id', Integer, ForeignKey('report.id'), nullable=False),
    Column('report_type_id', Integer, ForeignKey('report_type.id'), nullable=False),
    UniqueConstraint('report_id', 'report_type_id', name='report_report_type_uc')
)

class ReportType(Base):
    __tablename__ = 'report_type'
    
    id = Column(Integer, primary_key=True)
    extension = Column(String(8), unique=True, nullable=False)
    reports = relationship('Report', secondary=report_report_types, backref='report_types')

    def __init__(self, extension):
        self.extension = extension

class ReportAttribute(Base):
    __tablename__ = 'report_attribute'
    __table_args__ = (
        UniqueConstraint('report_id', 'name', name='report_name_uc'),
    )

    id = Column(Integer, primary_key=True)
    report_id = Column(Integer, ForeignKey('report.id'), nullable=False)
    name = Column(Unicode(255), nullable=False)
    value = Column(Unicode(255), nullable=False)

#    report = relationship('Report', backref=backref('attributes', order_by=id))

    def __init__(self, name, value):
        self.name = unicode(name)
        self.value = unicode(value)
