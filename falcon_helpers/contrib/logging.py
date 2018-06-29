import logging
import inspect

import wrapt

log = logging.getLogger(__name__)


def logrequest(level=logging.DEBUG):
    """Wrap resource functions or classes to get logging from called methods


    You can use it on a specific method...

        class MyResource:

            @logrequest(level=logging.INFO)
            def on_get(self, req, resp):
                # ...

    or on an entire class to decorate all falcon resource methods...

        @logrequest(level=logging.INFO)
        class MyResource:

            # Will be decorated
            def on_get(self, req, resp):
                # ...

            # Will be decorated
            def on_post(self, req, resp):
                # will be decorated
    """

    def handle_resource_func(wrapped, instance, args, kwargs):
        method_name = f'{instance.__class__.__name__}.{wrapped.__func__.__name__}'
        try:
            log.log(level, f'{method_name} called.')
            result = wrapped(*args, **kwargs)
        except Exception as e:
            name = e.__class__.__name__
            log.log(level, f'{method_name} raised {name}: {str(e)}.')
            raise
        else:
            log.log(level, f'{method_name} succeeded.')

        return result

    def handle_resource_class(wrapped, instance, args, kwargs):
        for method in ['__call__', 'on_get', 'on_post', 'on_put', 'on_delete']:
            m = getattr(wrapped, method, None)

            if m:
                setattr(wrapped, method, wrapt.FunctionWrapper(m, handle_resource_func))
        return wrapped(*args, **kwargs)

    @wrapt.decorator
    def logrequest(wrapped, instance, args, kwargs):
        if instance is None:
            if inspect.isclass(wrapped):
                # Decorator was applied to a class.
                return handle_resource_class(wrapped, instance, args, kwargs)
            else:
                # Decorator was applied to a function or staticmethod.
                log.warning(
                    'The logrequest decorator was not attached to an instance method or a '
                    'resource class. This is a noop.')
                return wrapped(*args, **kwargs)
        else:
            if inspect.isclass(instance):
                # Decorator was applied to a classmethod.
                log.warning(
                    'The logrequest decorator was attached to a classmethod or a this is a noop.'
                )
                return wrapped(*args, **kwargs)
            else:
                # Decorator was applied to an instancemethod.
                return handle_resource_func(wrapped, instance, args, kwargs)

    return logrequest


class Logging:

    def __init__(self, level=logging.INFO, fmt=None):
        self.log_level = level
        self.fmt = fmt or '[%(levelname)s] %(asctime)s - %(msg)s'

    def add_logger(self, name, handler, fmt=None, formatter=None, level=None):
        formatter = (
            logging.Formatter(fmt) if (fmt is not None and not formatter)
            else formatter if formatter
            else logging.Formatter(self.fmt)
        )

        handler.setFormatter(formatter)

        logger = logging.getLogger(name)
        logger.addHandler(handler)
        logger.setLevel(level or self.log_level)
