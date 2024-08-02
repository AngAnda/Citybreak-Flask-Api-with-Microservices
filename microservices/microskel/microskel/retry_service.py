import time
import random
from functools import wraps
from abc import ABC, abstractmethod
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RetryStrategy(ABC):
    @abstractmethod
    def wait(self, attempt: int):
        pass

class ExponentialBackoffStrategy(RetryStrategy):
    def __init__(self, base_wait_time: float):
        self.base_wait_time = base_wait_time

    def wait(self, attempt: int):
        logger.info(f'ExponentialBackoffStrategy wait: attempt {attempt}')
        wait_time = self.base_wait_time * (2 ** attempt)
        time.sleep(wait_time)

class RetryWithJitterStrategy(RetryStrategy):
    def __init__(self, base_wait_time: float, jitter: float):
        self.base_wait_time = base_wait_time
        self.jitter = jitter

    def wait(self, attempt: int):
        logger.info(f'RetryWithJitterStrategy wait: attempt {attempt}')
        wait_time = self.base_wait_time * (2 ** attempt)
        jitter = random.uniform(0, self.jitter)
        time.sleep(wait_time + jitter)

class RetryManager:
    def __init__(self):
        self.strategies = {
            'exponential_backoff': ExponentialBackoffStrategy(base_wait_time=1),
            'retry_with_jitter': RetryWithJitterStrategy(base_wait_time=1, jitter=1)
        }

    def get_strategy(self, strategy_name: str) -> RetryStrategy:
        strategy = self.strategies.get(strategy_name)
        if not strategy:
            raise ValueError(f"Retry strategy '{strategy_name}' not found.")
        return strategy

retry_manager = RetryManager()

def retry(strategy_name: str, max_retries=3):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            retry_strategy = retry_manager.get_strategy(strategy_name)
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    logger.warning(f"Retry attempt {attempt + 1} for {func.__name__} due to {e}")
                    retry_strategy.wait(attempt)
            raise last_exception
        return wrapper
    return decorator
