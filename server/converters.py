import re
from uuid import UUID

from werkzeug.routing import BaseConverter, ValidationError



class UUIDConverter(BaseConverter):

    def __init__(self, *args, **kwargs):
        """Custom UUID converter class.
            So we can use it in Flask routes like this:
                @app.route('/arbitrary/<uuid:capture_name>')
        """
        super().__init__(*args, **kwargs)

        self.UUID_RE = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$')

    def to_python(self, value: str) -> UUID:
        """to_python override, which handles conversion from an incoming capture to the view-function parameter."""
        if not self.UUID_RE.match(value):
            raise ValidationError()

        try:
            return UUID(value)
        except ValueError:
            raise ValidationError()

    def to_url(self, value: UUID) -> str:
        """to_url override, which handles conversion of a native UUID object into a string during Flask's url_for()."""
        return str(value)
