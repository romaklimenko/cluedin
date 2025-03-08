import requests

from .context import Context
from .env import CLUEDIN_REQUEST_TIMEOUT_IN_SECONDS


def get_vocab_keys(context: Context) -> list:
    """Get all vocabulary keys.

    Args:
        context (Context): Context object.

    Returns:
        list: JSON response - list of vocabulary keys.
    """

    headers = {
        'Authorization': f'Bearer {context.access_token}'
    }

    response = requests.get(
        url=f'{context.api_url}/entity/schema',
        headers=headers,
        timeout=CLUEDIN_REQUEST_TIMEOUT_IN_SECONDS,
        verify=context.verify_tls)

    response.raise_for_status()

    return response.json()
