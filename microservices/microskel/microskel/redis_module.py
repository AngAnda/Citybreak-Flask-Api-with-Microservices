from flask import Flask
from injector import Module, Binder, singleton
from redis import Redis
from decouple import config

class RedisBase:
    def __init__(self, redis_client: Redis):
        self.redis_client = redis_client

    def get(self, key):
        return self.redis_client.get(key)

    def set(self, key, value):
        self.redis_client.set(key, value)

class RedisModule(Module):
    def __init__(self, app: Flask):
        self.app = app

    def configure(self, binder: Binder) -> None:
        redis_client = self.configure_redis()
        binder.bind(Redis, to=redis_client, scope=singleton)
        binder.bind(RedisBase, to=RedisBase(redis_client), scope=singleton)

    def configure_redis(self):
        redis_host = config('REDIS_HOST', default='localhost')
        redis_port = config('REDIS_PORT', default=6379, cast=int)
        # redis_password = config('REDIS_PASSWORD', default=None)

        return Redis(
            host=redis_host,
            port=redis_port,
            # password=redis_password,
            decode_responses=True  # Optional, decodes responses to strings
        )

def configure_views(app):
    pass
