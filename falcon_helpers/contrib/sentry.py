import falcon
import raven


class Sentry:
    def __init__(self, dsn=None):
        self.set_dsn(dsn)

    def set_dsn(self, dsn):
        self.dsn = dsn
        self.client = raven.Client(dsn)

    def register(self, app):
        app.add_error_handler(Exception, self.handle)

    def handle(self, ex, req, resp, params):
        raisable = (falcon.http_error.HTTPError, falcon.http_status.HTTPStatus)

        if isinstance(ex, raisable):
            raise ex
        elif self.dsn:
            self.client.captureException(ex)
            raise falcon.HTTPInternalServerError()
        else:
            raise
