import time
from functools import wraps

def retry(max_retries=3, delay=5):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    retries += 1
                    print(f"Retry {retries}/{max_retries} failed: {e}")
                    time.sleep(delay)
            raise Exception(f"Failed after {max_retries} retries")
        return wrapper
    return decorator