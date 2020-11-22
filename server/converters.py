import re
import uuid

from werkzeug.routing import BaseConverter, ValidationError


class UUIDConverter(BaseConverter):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.UUID_RE = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$')

    def to_python(self, value):
        if not self.UUID_RE.match(value):
            raise ValidationError()

        try:
            return uuid.UUID(value)
        except ValueError:
            raise ValidationError()

    def to_url(self, value):
        return str(value)
