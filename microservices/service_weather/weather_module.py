from flask import Flask, jsonify, request
from injector import Injector
from redis import Redis
from datetime import datetime
import json
from microskel.redis_module import RedisBase, RedisModule

def configure_views(app):
    @app.route('/weather', methods=['POST'])
    def create(redis_base: RedisBase):
        keys = ('temperature', 'humidity', 'wind')
        weather = {k: request.form.get(k) for k in keys}
        city = request.form.get('city', 'Brasov')
        date = request.form.get('date', str(datetime.today().date()))
        key = f'{city}-{date}' if date else city

        redis_base.set(key, json.dumps(weather))
        return 'OK', 201

    @app.route('/weather', methods=['GET'])
    def get(redis_base: RedisBase):
        city = request.args.get('city')
        date = request.args.get('date')

        if not city and not date:
            all_keys = redis_base.client.keys('*')
            all_weather = {}
            for key in all_keys:
                weather = redis_base.get(key)
                all_weather[key] = json.loads(weather) if weather else None
            return jsonify(all_weather), 200

        key = f'{city}-{date}' if date else city
        weather = redis_base.get(key)
        if weather:
            return jsonify(json.loads(weather)), 200
        else:
            return jsonify({"error": "Data not found"}), 404