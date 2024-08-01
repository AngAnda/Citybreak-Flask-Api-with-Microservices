from injector import Module, Binder, singleton

from microskel.service_discovery import ServiceDiscovery  # interfata
import requests
from decouple import config

# se poate considera remote procedure call, remote server invocation
class ServiceOneProxy:  # TODO: frumos sa fie generate
    def __init__(self, service):
        self.service = service
    def get_hello(self, id):
        endpoint = self.service.injector.get(ServiceDiscovery).discover('service-events')
        response = requests.get(f'{endpoint.to_base_url()}/service_events/{id}')
        return response.json(), response.status_code

class ServiceTwoModule(Module):
    def __init__(self, service_two):
        self.service_two = service_two

    def configure(self, binder: Binder) -> None:
        service_one_client = ServiceOneProxy(self.service_two)
        binder.bind(ServiceOneProxy, to=service_one_client, scope=singleton)


def configure_views(app):
    @app.route('/events/<name>')
    def get_hello(name: str, service_one_client: ServiceOneProxy):
        app.logger.info(f'get_hello/{name} called in {config("MICROSERVICE_NAME")}')
        data_from_service_one = service_one_client.get_hello(name)
        return data_from_service_one
