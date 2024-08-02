from injector import Module, Binder, singleton

from microskel.service_discovery import ServiceDiscovery  # interfata
import requests
from decouple import config
from flask import request, jsonify


# se poate considera remote procedure call, remote server invocation

class ServiceWeatherProxy:
    def __init__(self, service):
        self.service = service

    def get_weather(self, city=None, date=None):
        endpoint = self.service.injector.get(ServiceDiscovery).discover('service_weather')
        if not endpoint:
            return {"error": "Service weather not found"}, 500

        base_url = endpoint.to_base_url()

        params = {}
        if city:
            params['city'] = city
        if date:
            params['date'] = date

        response = requests.get(f'{base_url}/weather', params=params)
        return response.json(), response.status_code

    def create_weather(self, data):
        endpoint = self.service.injector.get(ServiceDiscovery).discover('service_weather')
        response = requests.post(f'{endpoint.to_base_url()}/weather', data=data)
        return response.json(), response.status_code

    def update_weather(self, city, date, data):
        endpoint = self.service.injector.get(ServiceDiscovery).discover('service_weather')
        key = f'{city}-{date}' if date else city
        response = requests.put(f'{endpoint.to_base_url()}/weather/{key}', data=data)
        return response.json(), response.status_code

    def delete_weather(self, city, date):
        endpoint = self.service.injector.get(ServiceDiscovery).discover('service_weather')
        key = f'{city}-{date}' if date else city
        response = requests.delete(f'{endpoint.to_base_url()}/weather/{key}')
        return response.status_code

class ServiceTwoModule(Module):
    def __init__(self, service_two):
        self.service_two = service_two

    def configure(self, binder: Binder) -> None:
        service_one_client = ServiceWeatherProxy(self.service_two)
        binder.bind(ServiceWeatherProxy, to=service_one_client, scope=singleton)


def configure_views(app):
    @app.route('/weather', methods=['GET'])
    def get_weather(service_weather_client: ServiceWeatherProxy):
        city = request.args.get('city')
        date = request.args.get('date')
        app.logger.info(f'get_weather called with city={city} and date={date} in {config("MICROSERVICE_NAME")}')
        data_from_service_weather, status_code = service_weather_client.get_weather(city, date)
        return jsonify(data_from_service_weather), status_code

    @app.route('/weather', methods=['POST'])
    def create_weather(service_weather_client: ServiceWeatherProxy):
        data = request.form.to_dict()
        app.logger.info(f'create_weather called with data={data} in {config("MICROSERVICE_NAME")}')
        data_from_service_weather, status_code = service_weather_client.create_weather(data)
        return jsonify(data_from_service_weather), status_code

    @app.route('/weather', methods=['PUT'])
    def update_weather(service_weather_client: ServiceWeatherProxy):
        data = request.form.to_dict()
        city = request.args.get('city')
        date = request.args.get('date')
        app.logger.info(f'update_weather called with city={city}, date={date}, data={data} in {config("MICROSERVICE_NAME")}')
        data_from_service_weather, status_code = service_weather_client.update_weather(city, date, data)
        return jsonify(data_from_service_weather), status_code

    @app.route('/weather', methods=['DELETE'])
    def delete_weather(service_weather_client: ServiceWeatherProxy):
        city = request.args.get('city')
        date = request.args.get('date')
        app.logger.info(f'delete_weather called with city={city} and date={date} in {config("MICROSERVICE_NAME")}')
        data_from_service_weather, status_code = service_weather_client.delete_weather(city, date)
        return jsonify(data_from_service_weather), status_code
