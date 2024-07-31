from microskel.service_template import ServiceTemplate
import key_value_module


class ServiceOne(ServiceTemplate):
    def __init__(self, name):
        super().__init__(name)

    # def get_modules(self):
    #     return super().get_modules()  # + [key_value_module.KeyV]

    def get_python_modules(self):
        return super().get_python_modules() + [key_value_module]


if __name__ == '__main__':
    ServiceOne('service_one').start()
