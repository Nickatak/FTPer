"""Aggregate file for different base-classes to enable typehints."""

from sqlalchemy.ext.declarative.api import DeclarativeMeta #type: ignore
from werkzeug.datastructures import FileStorage
from werkzeug.wrappers import Response
