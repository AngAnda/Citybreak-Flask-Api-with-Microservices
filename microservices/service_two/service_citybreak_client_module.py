from injector import Module, Binder, singleton

from microskel.service_discovery import ServiceDiscovery  # interfata
import requests
from decouple import config
from flask import request, jsonify


# se poate considera remote procedure call, remote server invocation

class ServiceCitybreakProxy:
    def __init__(self, service):
        self.service = service

    def get_weather(self, city=None, date=None):
        endpoint = self.service.injector.get(ServiceDiscovery).discover('service-weather')
        base_url = endpoint.to_base_url()

        params = {}
        if city:
            params['city'] = city
        if date:
            params['date'] = date

        response = requests.get(f'{base_url}/weather', params=params)
        return response.json(), response.status_code

    def get_events(self, city=None, date=None):
        endpoint = self.service.injector.get(ServiceDiscovery).discover('service-events')
        base_url = endpoint.to_base_url()

        params = {}
        if city:
            params['city'] = city
        if date:
            params['date'] = date

        response = requests.get(f'{base_url}/service_events', params=params)
        return response.json(), response.status_code


class ServiceCitybreakModule(Module):
    def __init__(self, service_two):
        self.service_two = service_two

    def configure(self, binder: Binder) -> None:
        service_one_client = ServiceCitybreakProxy(self.service_two)
        binder.bind(ServiceCitybreakProxy, to=service_one_client, scope=singleton)


def configure_views(app):
    @app.route('/citybreak', methods=['GET'])
    def get_citybreak(service_citybreak_client: ServiceCitybreakProxy):
        city = request.args.get('city')
        date = request.args.get('date')
        app.logger.info(f'get_citybreak called with city={city} and date={date} in {config("MICROSERVICE_NAME")}')

        weather_data, weather_status = service_citybreak_client.get_weather(city, date)
        events_data, events_status = service_citybreak_client.get_events(city, date)

        if weather_status == 200 and events_status == 200:
            return jsonify({
                'weather': weather_data,
                'events': events_data
            }), 200
        else:
            error_message = {}
            if weather_status != 200:
                error_message['weather'] = 'Error fetching weather data'
            if events_status != 200:
                error_message['events'] = 'Error fetching events data'
            return jsonify(error_message), max(weather_status, events_status)
