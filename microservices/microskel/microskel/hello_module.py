from flask import jsonify
from injector import Module, Binder, singleton


class HelloService:
    def __init__(self, greet: str):
        self.greet = greet

    def say_hello(self, name):
        return jsonify(f'{self.greet}, {name}')


class HelloModule(Module):
    def configure(self, binder: Binder) -> None:
        hello = HelloService('Hello')
        binder.bind(HelloService, hello, scope=singleton)


def configure_views(app):
    @app.route('/hello/<name>', methods=['GET'])
    def say_hello(name: str, hello: HelloService):
        app.logger.info(f'/hello/{name} was called')
        return hello.say_hello(name)
