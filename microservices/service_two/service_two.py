from microskel.service_template import ServiceTemplate
import service_one_client_module
import service_weather_client_module
import service_citybreak_client_module

class ServiceTwo(ServiceTemplate):

    def get_modules(self):
        return super().get_modules() + [
            service_one_client_module.ServiceTwoModule(self),
            service_weather_client_module.ServiceTwoModule(self),
            service_citybreak_client_module.ServiceCitybreakModule(self)
        ]

    def get_python_modules(self):
        return (super().get_python_modules() +
                [service_one_client_module, service_weather_client_module, service_citybreak_client_module])


if __name__ == '__main__':
    ServiceTwo().start()