from injector import Module, Binder
from decouple import config


class HealthModule(Module):
    def configure(self, binder: Binder) -> None:
        pass


def configure_views(app):
    @app.route('/health', methods=['GET'])
    def health():
        app.logger.info(f'/health was called for {config("MICROSERVICE_NAME")}')
        return 'Health status: OK', 200
