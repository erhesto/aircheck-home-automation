import logging
import requests
from functools import wraps


def handle_exceptions(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        response = func(*args, **kwargs)

        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            logging.error(e.args[0])
            exit()

        try:
            response.json()
        except ValueError as e:
            logging.error('Cannot decode json: %s', e.args[0])
            exit()

        return response.json()
    return wrapper
