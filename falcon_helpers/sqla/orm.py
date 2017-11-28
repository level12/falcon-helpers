import sqlalchemy as sa
from sqlalchemy.schema import MetaData
from sqlalchemy.ext.declarative import as_declarative

from falcon_helpers.sqla.core import utcnow


convention = {
  "ix": 'ix_%(column_0_label)s',
  "uq": "uq_%(table_name)s_%(column_0_name)s",
  "ck": "ck_%(table_name)s_%(constraint_name)s",
  "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
  "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)


@as_declarative(metadata=metadata)
class ModelBase:
    pass


class BaseColumns:
    id = sa.Column(sa.Integer, primary_key=True, nullable=False)

    created_ts = sa.Column(sa.DateTime, server_default=utcnow())
    updated_ts = sa.Column(sa.DateTime, server_default=utcnow(),
                           server_onupdate=utcnow())
