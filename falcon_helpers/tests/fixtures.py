import mock
import pytest
import sqlalchemy as sa

import falcon_helpers.sqla.db as db

bind = sa.engine.create_engine('sqlite://')
Base = sa.ext.declarative.declarative_base(bind=bind)

db.session.configure(bind=bind)


@pytest.fixture()
def mocked_sentry_client():
    with mock.patch('falcon_helpers.plugins.sentry.raven.Client',
                    spec_set=True, autospec=True) as m:
        yield m
