from injector import Module, Binder, singleton

from microskel.service_discovery import ServiceDiscovery  # interfata
import requests
from decouple import config
from flask import request, jsonify

# se poate considera remote procedure call, remote server invocation

class ServiceOneProxy:  # TODO: frumos sa fie generate
    def __init__(self, service):
        self.service = service
    def get_events(self, id):
        endpoint = self.service.injector.get(ServiceDiscovery).discover('service-events')
        response = requests.get(f'{endpoint.to_base_url()}/service_events/{id}')
        return response.json(), response.status_code

    def create_event(self, data):
        endpoint = self.service.injector.get(ServiceDiscovery).discover('service-events')
        response = requests.post(f'{endpoint.to_base_url()}/service_events', data=data)
        return response.json(), response.status_code

    def update_event(self, id, data):
        endpoint = self.service.injector.get(ServiceDiscovery).discover('service-events')
        response = requests.put(f'{endpoint.to_base_url()}/service_events/{id}', data=data)
        return response.json(), response.status_code

    def delete_event(self, id):
        endpoint = self.service.injector.get(ServiceDiscovery).discover('service-events')
        response = requests.delete(f'{endpoint.to_base_url()}/service_events/{id}')
        return response.status_code

class ServiceTwoModule(Module):
    def __init__(self, service_two):
        self.service_two = service_two

    def configure(self, binder: Binder) -> None:
        service_one_client = ServiceOneProxy(self.service_two)
        binder.bind(ServiceOneProxy, to=service_one_client, scope=singleton)


def configure_views(app):
    @app.route('/events/<id>')
    def get_events(id: str, service_one_client: ServiceOneProxy):
        app.logger.info(f'get_hello/{id} called in {config("MICROSERVICE_NAME")}')
        data_from_service_one = service_one_client.get_events(id)
        return data_from_service_one

    @app.route('/events', methods=['POST'])
    def create_event(service_one_client: ServiceOneProxy):
        data = request.form.to_dict()
        app.logger.info(f'create_event called with data={data} in {config("MICROSERVICE_NAME")}')
        data_from_service_one, status_code = service_one_client.create_event(data)
        return jsonify(data_from_service_one), status_code

    @app.route('/events/<id>', methods=['PUT'])
    def update_event(id: str, service_one_client: ServiceOneProxy):
        data = request.form.to_dict()
        app.logger.info(f'update_event/{id} called with data={data} in {config("MICROSERVICE_NAME")}')
        data_from_service_one, status_code = service_one_client.update_event(id, data)
        return jsonify(data_from_service_one), status_code

    @app.route('/events/<id>', methods=['DELETE'])
    def delete_event(id: str, service_one_client: ServiceOneProxy):
        app.logger.info(f'delete_event/{id} called in {config("MICROSERVICE_NAME")}')
        data_from_service_one, status_code = service_one_client.delete_event(id)
        return jsonify(data_from_service_one), status_code
