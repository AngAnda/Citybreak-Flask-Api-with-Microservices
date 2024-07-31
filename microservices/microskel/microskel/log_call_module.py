import functools
from flask import Flask
from injector import Module, singleton, Binder


app: Flask = None  # TODO bind via a class


def log_call(f):
    global app

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        res = exc = None
        try:
            res = f(*args, **kwargs)
            return res
        except Exception as e:
            exc = e
        finally:  # always executes
            params = ', '.join([repr(a) for a in args])
            params += ', '.join([f'{k}={repr(v)}' for k, v in kwargs.items()])
            log = f'Call to {f.__name__}({params}) '
            log += f'gives {res}' if not exc else 'raises {type(exc)}: {exc}'
            if app:
                app.logger.debug(log)
            if exc:
                raise exc
    return wrapper


class LogCallModule(Module):
    def __init__(self, flask_app: Flask):
        global app
        app = flask_app


def configure_views(app):
    pass
