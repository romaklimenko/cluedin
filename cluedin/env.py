from os import environ

CLUEDIN_REQUEST_TIMEOUT = environ.get('CLUEDIN_REQUEST_TIMEOUT', 60 * 5)
