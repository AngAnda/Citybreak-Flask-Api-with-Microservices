class HostAndPort:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def to_base_url(self):
        return f'http://{self.host}:{self.port}'

    def str(self):
        return repr(self)

    def repr(self):
        return f'{self.host}:{self.port}'


class ServiceDiscovery:
    def discover(self, service_name: str) -> HostAndPort:
        pass
