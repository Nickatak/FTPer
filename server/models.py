"""SQLAlchemy models for our server to interact with PostgreSQL."""
import datetime
import uuid

import sqlalchemy #type: ignore
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.dialects.postgresql import UUID as psUUID #type: ignore
from sqlalchemy.ext.declarative import declarative_base #type: ignore
from sqlalchemy.orm import relationship #type: ignore

from conf import DB_URL
from server.types import DeclarativeMeta

Base: DeclarativeMeta = declarative_base()

class DBManager(object):
    def __init__(self) -> None:
        """Creates a DBManager instance.
            This class is used as a friendliness-wrapper so we can easily use the sqlalchemy session.
        """

        engine = sqlalchemy.create_engine(DB_URL)
        self.session = sqlalchemy.orm.scoped_session(sqlalchemy.orm.sessionmaker())
        self.session.configure(bind=engine, autoflush=False, expire_on_commit=False)

        Base.metadata.create_all(engine)

class User(Base):
    """User class, a simple container to hold relevant information from Discord's API."""

    # We don't actually need this table, we could've just used the Snowflake id from Discord, but I think that this makes it a bit cleaner incase we want to implement some additional features (EG: emails) or something later on down the line.
    __tablename__ = 'users'

    # So a User's ID implemented by discord is a 64-bit uint.  Unfortunately, postgreSQL (just my arbitrary [for now] choice of SQL variant) doesn't handle unsigned 64b ints (BIGINT is signed for their implementation) so we're going to have to use NUMERIC to support arbitrarily large id's, at a considerable performance tradeoff.  I'm afraid this is going to cost us by making joins (a frequent operation in this application) really expensive.  If this gets too slow, what I think I'll do is use a 8-bytea field and just interface with the Snowflake (id) in my application-level by transforming the snowflake into hex first, instead of using the DB-level interactions.
    id = Column(Numeric, primary_key=True)
    name = Column(String(32)) # discord.User.name (EG: Nickatak), max is 32 chars
    discrim = Column(String) # discord.User.discriminator (EG: #1337)

class File(Base):
    """File class.  This holds relevant information for each user's uploaded file."""

    __tablename__ = 'files'

    # Just a bit of obfuscation really.  I'll make a "prettifier" for this (B64 maybe).
    id = Column(psUUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False, unique=True)
    # This is marked "completed" if a file has been uploaded (so it can be downloaded by others).
    completed = Column(Boolean, default=False)
    ext = Column(String) #File extension, INCLUDING the period (EG: '.blah')

    user_id = Column(Numeric, ForeignKey('users.id'))
    user = relationship('User', foreign_keys='File.user_id', backref='files')

    # This will be used for our chron-job "cleaner" later, so we can use an "expiration" time for the files.
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
