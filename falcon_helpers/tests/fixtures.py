import sqlalchemy as sa

import falcon_helpers.sqla.db as db

bind = sa.engine.create_engine('sqlite://')
Base = sa.ext.declarative.declarative_base(bind=bind)

db.session.configure(bind=bind)
