import json

from sqlalchemy import Text
from sqlalchemy.types import TypeDecorator


class PortableJSON(TypeDecorator):
    """JSON guardado como texto, para funcionar igual no PostgreSQL e no Db2."""

    impl = Text
    cache_ok = True

    def process_bind_param(self, value, dialect):
        return None if value is None else json.dumps(value, ensure_ascii=False)

    def process_result_value(self, value, dialect):
        return None if value is None else json.loads(value)
