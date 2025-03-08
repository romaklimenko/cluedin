import requests

from .context import Context
from .env import CLUEDIN_REQUEST_TIMEOUT_IN_SECONDS


def get_entity_blob(context: Context, entity_id: str) -> str:
    """Get entity blob.

    Args:
        context (Context): Context object.
        entity_id (str): Entity ID.

    Returns:
        dict: XML response - entity blob.
    """

    headers = {
        'Authorization': f'Bearer {context.access_token}'
    }

    params = {
        'id': entity_id
    }

    response = requests.get(
        url=f'{context.api_url}/admin/entity/blob',
        headers=headers,
        params=params,
        timeout=CLUEDIN_REQUEST_TIMEOUT_IN_SECONDS,
        verify=context.verify_tls)

    response.raise_for_status()

    return response.text


def get_entity_as_clue(context: Context, entity_id: str) -> str:
    """Get entity as clue.

    Args:
        context (Context): Context object.
        entity_id (str): Entity ID.

    Returns:
        dict: XML response - entity clue.
    """

    headers = {
        'Authorization': f'Bearer {context.access_token}'
    }

    params = {
        'id': entity_id
    }

    response = requests.get(
        url=f'{context.api_url}/admin/entity/clue',
        headers=headers,
        params=params,
        timeout=CLUEDIN_REQUEST_TIMEOUT_IN_SECONDS,
        verify=context.verify_tls)

    response.raise_for_status()

    return response.text
