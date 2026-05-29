import time
from typing import Callable, Any, Type

def retry_on_failure(
    func: Callable[..., Any],
    max_attempts: int = 3,
    delay_seconds: float = 1.0,
    *args,
    exception_types: tuple[Type[Exception], ...] = (Exception,)
) -> Any:
    """
    Retries the execution of a function upon failure.

    Args:
        func: The function to execute.
        max_attempts: The maximum number of times to attempt the function call.
        delay_seconds: The time to wait between attempts in seconds.
        *args: Positional arguments to pass to the function.
        exception_types: A tuple of exception types to catch and retry on.
                          Defaults to catching any Exception.

    Returns:
        The result of the function if successful.

    Raises:
        The last encountered exception if all attempts fail.
    """
    last_exception = None
    for attempt in range(max_attempts):
        try:
            print(f"Attempt {attempt + 1}/{max_attempts}...")
            return func(*args)
        except exception_types as e:
            last_exception = e
            if attempt < max_attempts - 1:
                print(f"Attempt failed with {type(e).__name__}: {e}. Retrying in {delay_seconds} seconds...")
                time.sleep(delay_seconds)
            else:
                print("All attempts failed.")
                raise last_exception
        except Exception as e:
            # Catch any other unexpected exception and stop trying
            print(f"Caught unexpected exception {type(e).__name__} on attempt {attempt + 1}. Stopping retries.")
            raise e

# Example Usage (Self-contained for demonstration)
def unreliable_service_call():
    if not hasattr(unreliable_service_call, 'count'):
        unreliable_service_call.count = 0
    unreliable_service_call.count += 1
    if unreliable_service_call.count < 3:
        raise ConnectionError("Service unavailable")
    return "Success after retries"

if __name__ == '__main__':
    try:
        result = retry_on_failure(
            unreliable_service_call,
            max_attempts=5,
            delay_seconds=0.5,
            exception_types=(ConnectionError,)
        )
        print(f"Final Result: {result}")
    except Exception as e:
        print(f"Operation failed permanently: {type(e).__name__}: {e}")