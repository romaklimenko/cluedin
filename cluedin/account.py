import requests

from .context import Context
from .env import CLUEDIN_REQUEST_TIMEOUT

# Account


def get_users(context: Context, org_id: str = None) -> dict:
    """Get users for an organization.

    Args:
        context (Context): Context object.
        org_id (str, optional): organization ID. Defaults to None.
            If None, the current user's organization ID is used.

    Returns:
        dict: JSON response.
    """
    headers = {
        'Authorization': f'Bearer {context.access_token}'
    }

    params = {}

    if org_id is not None:
        params['organizationId'] = org_id

    response = requests.get(
        url=f'{context.auth_url}/api/account/accounts',
        headers=headers,
        params=params,
        timeout=CLUEDIN_REQUEST_TIMEOUT,
        verify=context.verify_tls)

    if not response.ok:
        response.raise_for_status()

    return response.json()


# Availability

def is_organization_available_response(context: Context, org_name: str) -> dict:
    """Check if an organization name is available.

    Args:
        context (Context): Context object.
        org_name (str): Organization name.

    Returns:
        dict: JSON response.
    """
    headers = {
        'Authorization': f'Bearer {context.access_token}'
    }
    response = requests.get(
        url=f'{context.auth_url}/api/account/available?clientId={org_name}',
        headers=headers,
        timeout=CLUEDIN_REQUEST_TIMEOUT,
        verify=context.verify_tls)

    if not response.ok:
        response.raise_for_status()

    return response.json()


def is_organization_available(context: Context, org_name: str) -> bool:
    """Check if an organization name is available.

    Args:
        context (Context): Context object.
        org_name (str): Organization name.

    Returns:
        bool: True if available, False otherwise.
    """
    return bool(is_organization_available_response(context, org_name)['isAvailable'])


def is_user_available_response(context: Context, user_email: str, org_name: str) -> dict:
    """Check if a user email is available.

    Args:
        context (Context): Context object.
        user_email (str): User email.
        org_name (str): Organization name.

    Returns:
        dict: JSON response.
    """
    response = requests.get(
        url=f'{context.auth_url}/api/account/username?username={user_email}&clientId={org_name}',
        timeout=CLUEDIN_REQUEST_TIMEOUT,
        verify=context.verify_tls)

    if not response.ok:
        response.raise_for_status()

    return response.json()


def is_user_available(context: Context, user_email: str, org_name: str) -> bool:
    """Check if a user email is available.

    Args:
        context (Context): Context object.
        user_email (str): User email.
        org_name (str): Organization name.

    Returns:
        bool: True if available, False otherwise.
    """
    return bool(is_user_available_response(context, user_email, org_name)['isAvailable'])
