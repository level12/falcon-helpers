import pytest

import falcon_helpers.app as fhapp
from falcon_helpers.middlewares.multi import MultiMiddleware


def test_enables_dynamic_middleware():

    app = fhapp.App()
    assert isinstance(app._middleware[0][0].__self__, MultiMiddleware)
    assert isinstance(app._middleware[1][0].__self__, MultiMiddleware)
    assert isinstance(app._middleware[2][0].__self__, MultiMiddleware)

    with pytest.raises(RuntimeError):
        app = fhapp.App(independent_middleware=False)

    app = fhapp.App(enable_dynamic_mw=False)
    assert app._middleware == ((), (), (),)
