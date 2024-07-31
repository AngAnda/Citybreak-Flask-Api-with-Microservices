from injector import Module
from logstash import TCPLogstashHandler
from decouple import config


class LoggingModule(Module):
    def __init__(self, app):
        if config('LOGSTASH_ENABLED', cast=bool):
            logstash_handler = TCPLogstashHandler(host=config('LOGSTASH_AGENT_HOST'),
                                                  port=config('LOGSTASH_AGENT_PORT', cast=int),
                                                  message_type='logstash', version=1)
            app.logger.addHandler(logstash_handler)


def configure_views(app):
    pass
