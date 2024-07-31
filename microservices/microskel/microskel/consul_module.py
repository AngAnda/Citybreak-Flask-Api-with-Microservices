import time

from injector import *
import consul
from decouple import config
import uuid
import time

class ConsulRegistrator:
    def __init__(self, app):
        self.app = app
        self.agent_client = consul.Consul(host=config('CONSUL_HOST'), verify=False,
                                          port=config('CONSUL_PORT', cast=int)).agent
        self.host = config('MICROSERVICE_HOST') # nu localhost
        self.port = config('MICROSERVICE_PORT', cast=int)
        self.name = config('MICROSERVICE_NAME')
        self.id = f'{self.name} - {uuid.uuid4()}'  # unic per cluster
        self.registered = False

    def register(self):
        self.app.logger.info(f'Registering {self.id} to Consul agent...')
        try:
            health_url = f'http://{self.host}:{self.port}/health'
            check_endpoint = consul.Check.http(url=health_url,
                                               interval=config('CONSUL_CHECK_INTERVAL'),
                                               timeout=config('CONSUL_CHECK_TIMEOUT'))
            self.agent_client.service.register(
                name=self.name, service_id=self.id, port=self.port, address=self.host,
                check=check_endpoint)
        except Exception as e:
            self.app.logger.error(f'Cannot register to consul: {e}: {self.id}')
            time.sleep(2)
            self.register()
        else:
            self.app.logger.info(f'Successfully registered {self.id} to Consul Agent')
            self.registered = True

    def deregister(self):
        self.app.logger.info(f'Deregistering {self.id}...')
        if self.registered:
            self.agent_client.service.deregister(self.id)
            self.app.logger.info(f'Successfully deregistered {self.id}')
            self.registered = False
        else:
            self.app.logger.error('I am already deregistered')


class ConsulLifecycleListener:
    def __init__(self, consul_registrator: ConsulRegistrator):
        self.consul_registrator = consul_registrator

    def lifecycle_started(self):
        self.consul_registrator.register()

    def lifecycle_stopped(self):
        self.consul_registrator.deregister()


class ConsulModule(Module):
    def __init__(self, app):
        self.app = app

    def configure(self, binder: Binder) -> None:
        registrator = ConsulRegistrator(self.app)
        listener = ConsulLifecycleListener(registrator)
        binder.bind(ConsulRegistrator, to=registrator, scope=singleton)
        binder.bind(ConsulLifecycleListener, to=listener, scope=singleton)


def configure_views(app):
    pass
