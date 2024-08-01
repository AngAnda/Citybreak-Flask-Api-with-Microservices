from microskel.service_template import ServiceTemplate
import service_events_client_module


class ServiceGateway(ServiceTemplate):

    def get_modules(self):
        return super().get_modules() + [service_events_client_module.ServiceEventsModule(self)]

    def get_python_modules(self):
        return super().get_python_modules() + [service_events_client_module]

    def custom_function(self, id):  # ca si exemplu
         data = self.injector.get(service_events_client_module.ServiceEventsProxy).get_events(id)
         return data


if __name__ == '__main__':
    ServiceGateway().start()