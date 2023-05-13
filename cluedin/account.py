import requests
from .context import Context
from .env import CLUEDIN_REQUEST_TIMEOUT

# Account


def get_users(context: Context, org_id: str = None) -> str:
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
        timeout=CLUEDIN_REQUEST_TIMEOUT)

    if not response.ok:
        response.raise_for_status()

    return response.json()


# Availability

def is_organization_available_response(context: Context, org_name: str) -> str:
    headers = {
        'Authorization': f'Bearer {context.access_token}'
    }
    response = requests.get(
        url=f'{context.auth_url}/api/account/available?clientId={org_name}',
        headers=headers,
        timeout=CLUEDIN_REQUEST_TIMEOUT)

    if not response.ok:
        response.raise_for_status()

    return response.json()


def is_organization_available(context: Context, org_name: str) -> bool:
    return bool(is_organization_available_response(context, org_name)['isAvailable'])


def is_user_available_response(context: Context, user_email: str, org_name: str) -> str:
    response = requests.get(
        url=f'{context.auth_url}/api/account/username?username={user_email}&clientId={org_name}',
        timeout=CLUEDIN_REQUEST_TIMEOUT)
    if not response.ok:
        response.raise_for_status()

    return response.json()


def is_user_available(context: Context, user_email: str, org_name: str) -> bool:
    return bool(is_user_available_response(context, user_email, org_name)['isAvailable'])
