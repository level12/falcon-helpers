import falcon

from falcon_helpers.config import Config


class API(falcon.API):
    __slots__ = (
        'config',
        'plugins',
    )

    @classmethod
    def from_inis(cls, *paths, api_kwargs=None):
        """Create an instance of the API from configuration files"""

        app = cls(**(api_kwargs or {}))

        app.config = Config.from_inis(*paths)

        return app
