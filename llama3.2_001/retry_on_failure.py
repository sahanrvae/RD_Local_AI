import time
from typing import Callable
import os

def retry_on_failure(func: Callable, max_attempts: int = 3, sleep_seconds: float = 1.0) -> Callable:
    """
    A decorator that retries the function on failure.

    Args:
        func (Callable): The function to be decorated.
        max_attempts (int, optional): The maximum number of attempts. Defaults to 3.
        sleep_seconds (float, optional): The time to sleep between attempts in seconds. Defaults to 1.0.

    Returns:
        Callable: The decorated function.
    """
    def wrapper(*args, **kwargs) -> Any:
        for attempt in range(max_attempts):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(f"Attempt {attempt+1} failed with error: {e}")
                time.sleep(sleep_seconds)
        raise Exception(f"Failed after {max_attempts} attempts")

    # Check if the function is already decorated
    if wrapper.__name__ == func.__name__ + "_wrapper":
        return func

    def new_func(*args, **kwargs) -> Any:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"Attempt 1 failed with error: {e}")
            os.makedirs('./filles', exist_ok=True)

    wrapper.__name__ = func.__name__ + "_wrapper"
    new_func.__name__ = func.__name__
    return new_func