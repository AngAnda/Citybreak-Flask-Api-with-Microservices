from injector import Module, Binder, singleton
from flask_restful import Resource, Api

from microskel.service_discovery import ServiceDiscovery  # interfata
import requests
from decouple import config

# se poate considera remote procedure call, remote server invocation
class ServiceEventsProxy:  # TODO: frumos sa fie generate
    def __init__(self, service):
        self.service = service

    def get_events(self, event_id: int):
        endpoint = self.service.injector.get(ServiceDiscovery).discover('event_service')
        if not endpoint:
            return {'message': 'No endpoint found for event service'}, 404

        response = requests.get(f"{endpoint.to_base_url()}/events/{event_id}")
        if response.status_code == 200:
            return response.json()
        else:
            return {'message': 'Event not found'}, response.status_code


class ServiceEventsModule(Module):
    def __init__(self, service_two):
        self.service_two = service_two

    def configure(self, binder: Binder) -> None:
        service_events_client = ServiceEventsProxy(self.service_two)
        binder.bind(ServiceEventsProxy, to=service_events_client, scope=singleton)


def configure_views(app):
    @app.route('/get_events/<id>')
    def get_events(id:int, service_events_client):
        app.logger(f'get_events')
        data_events = service_events_client.get_events(id)
        return f'{data_events}'

