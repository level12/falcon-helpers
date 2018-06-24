import falcon
import raven


class SentryPlugin:
    """Simple Sentry integration plugin

        config = {'sentry_dsn': 'some@sentry.io'}
        app = falcon.API()
        sentry = SentryPlugin(config['sentry_dsn'])
        sentry.register_app(sentry)

    You can get access to this globally so that you can capture exceptions without it having to get
    all the way up to the Falcon layer again.  Any exception that is caught by the falcon error
    handler will be sent to sentry (except HTTPError's and HTTPStatus's).

        sentry = Sentry()

        def create_app(config):
            app = falcon.API()

            sentry.set_dsn(config.sentry_dsn)
            sentry.register(app)
            return app


        class SomeResource:

            def on_get(self, req, resp):
                try:
                    some_failure()
                except Exception as e:
                    sentry.captureException(e)
                    pass
    """

    @property
    def dsn(self):
        return self._dsn

    @dsn.setter
    def dsn(self, dsn):
        self._dsn = dsn
        self.client = raven.Client(dsn)

    def __init__(self, dsn=None):
        self.dsn = dsn

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
