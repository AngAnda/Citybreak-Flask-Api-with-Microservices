from flask import Flask
import logging
import atexit
import signal
import sys

from decouple import config
from flask_injector import FlaskInjector
from injector import Injector

import microskel.hello_module
import microskel.db_module
import microskel.consul_module
import microskel.health_module
import microskel.logging_module
import microskel.consul_discovery_module
import microskel.log_call_module


class ServiceTemplate:
    def __init__(self, name=__name__):
        self.app = Flask(name)
        self.app.logger.addHandler(logging.StreamHandler())
        self.app.logger.level = logging.DEBUG
        self.injector = None  # optional (design decision)

    def get_modules(self):  # polymorphic function call
        modules = [
                microskel.log_call_module.LogCallModule(self.app),
                microskel.hello_module.HelloModule(),
                microskel.consul_module.ConsulModule(self.app), microskel.health_module.HealthModule(),
                microskel.logging_module.LoggingModule(self.app),
                microskel.consul_discovery_module.ConsulDiscoveryModule(self.app)]
        if config('USE_DB', cast=bool):
            modules.append(microskel.db_module.DatabaseModule(self.app))
        return modules

    def get_python_modules(self):
        return [microskel.log_call_module,
                microskel.hello_module,
                microskel.consul_module,
                microskel.health_module,
                microskel.db_module,
                microskel.logging_module,
                microskel.consul_discovery_module]

    def start(self):
        def before_shutdown():
            self.injector.get(microskel.consul_module.ConsulLifecycleListener).lifecycle_stopped()

        def app_killed():
            self.injector.get(microskel.consul_module.ConsulLifecycleListener).lifecycle_stopped()
            sys.exit(0)

        atexit.register(before_shutdown)
        signal.signal(signal.SIGTERM, app_killed)
        signal.signal(signal.SIGINT, app_killed)
        signal.signal(signal.SIGABRT, app_killed)

        with self.app.app_context():
            self.injector = Injector(self.get_modules())
            for m in self.get_python_modules():
                m.configure_views(self.app)
            FlaskInjector(app=self.app, injector=self.injector)

        self.injector.get(microskel.consul_module.ConsulLifecycleListener).lifecycle_started()  # not 100% ok

        self.app.run(host=config('MICROSERVICE_HOST'),
                     port=config('MICROSERVICE_PORT', cast=int),
                     debug=config('MICROSERVICE_DEBUG', cast=bool))

    def test(self):  # optional
        client = self.app.test_client()
        display(client.get('/hello/Gigi'))


def display(response):
    print(f'{response.status}\n{response.headers}\n{response.data}')
