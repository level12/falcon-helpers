import falcon.testing
import unittest.mock as mock
import pytest

from falcon_helpers.plugins import SentryPlugin


class FakeException(Exception):
    pass


@pytest.fixture()
def app():
    app = falcon.API()

    class FakeResource:
        def on_get(self, req, resp):
            raise FakeException('Failed')

    app.add_route('/fails', FakeResource())

    return app


@pytest.fixture()
def client(app):
    return falcon.testing.TestClient(app)


def test_sentry(mocked_sentry_client, client):
    plugin = SentryPlugin('test_dsn')
    plugin.register(client.app)

    client.simulate_get('/fails')
    name, args, kwargs = mocked_sentry_client.method_calls[0]

    assert plugin.dsn == 'test_dsn'
    assert isinstance(args[0], FakeException)
