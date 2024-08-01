from microskel.service_template import ServiceTemplate
import weather_module

class ServiceWeather(ServiceTemplate):
    def __init__(self, name):
        super().__init__(name)

    def get_modules(self):
        return super().get_modules()
    def get_python_modules(self):
        return super().get_python_modules() + [weather_module]

if __name__ == '__main__':
    ServiceWeather('service-weather').start()
