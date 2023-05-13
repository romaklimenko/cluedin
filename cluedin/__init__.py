from os import environ

from .context import Context

from . import account
from . import context
from . import gql
from . import public
from . import utils

CLUEDIN_REQUEST_TIMEOUT = environ.get('CLUEDIN_REQUEST_TIMEOUT', 60 * 5)
