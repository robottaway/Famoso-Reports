import os
import sha

from sqlalchemy import (
    Column,
    Integer,
    Unicode
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

class User(Base):
    __tablename__ = 'appusers'
    id = Column(Integer, primary_key=True)
    username = Column(Unicode(20), unique=True, nullable=False)
    password = Column(Unicode(80), nullable=False)
    email = Column(Unicode(256), nullable=False)

    def __init__(self, username=None, password=None, email=None):
        self.username = username
        self.email = email
        if password:
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
