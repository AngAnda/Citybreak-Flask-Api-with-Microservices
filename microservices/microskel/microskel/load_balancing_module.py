# load_balancer_decorator.py
import random
import logging

# Set up basic logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LoadBalancerDecorator:
    def __init__(self, strategy='round_robin'):
        self.strategy = strategy
        self.counters = {}
        self.connection_counts = {}

    def __call__(self, func):
        def wrapped(instance, service_name, *args, **kwargs):
            logger.info(f"Discover called for service: {service_name} with strategy: {self.strategy}")
            registrations = instance.services.get(service_name)
            if not registrations:
                logger.info(
                    f"No registrations found for service: {service_name}. Falling back to original discover method.")
                return func(instance, service_name, *args, **kwargs)

            if self.strategy == 'round_robin':
                selected = self.round_robin(service_name, registrations)
            elif self.strategy == 'least_connections':
                selected = self.least_connections(instance, service_name, registrations)
            else:
                selected = random.choice(registrations)

            logger.info(f"Selected registration for service {service_name}: {selected}")
            return selected

        return wrapped

    def round_robin(self, service_name, registrations):
        if service_name not in self.counters:
            self.counters[service_name] = 0
        index = self.counters[service_name]
        self.counters[service_name] = (index + 1) % len(registrations)
        logger.info(f"Round Robin selected index {index} for service {service_name}")

        return registrations[index]

    def least_connections(self, instance, service_name, registrations):
        min_connections = min(instance.connection_counts[service_name].values())
        for reg in registrations:
            if instance.connection_counts[service_name][reg] == min_connections:
                instance.connection_counts[service_name][reg] += 1
                logger.info(f"Least Connections selected registration {reg} for service {service_name}")
                return reg
