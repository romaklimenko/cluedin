import requests
from .context import Context

# Account


def get_users(context: Context, org_id: str = None) -> str:
    headers = {
        'Authorization': 'Bearer {}'.format(context.access_token)
    }

    params = {}

    if org_id is not None:
        params['organizationId'] = org_id

    response = requests.get(
        url=f'{context.auth_url}/api/account/accounts',
        headers=headers,
        params=params)

    if not response.ok:
        raise Exception({
            'status_code': response.status_code,
            'text': response.text
        })

    return response.json()


# Availability

def is_organization_available_response(context: Context, organization):
    headers = {
        'Authorization': 'Bearer {}'.format(context.access_token)
    }
    response = requests.get(
        url=f'{context.auth_url}/api/account/available?clientId={organization}',
        headers=headers)

    if not response.ok:
        raise Exception({
            'status_code': response.status_code,
            'text': response.text
        })

    return response.json()


def is_organization_available(context: Context, organization):
    return is_organization_available_response(context, organization)['isAvailable']


def is_user_available_response(context, user, organization):
    response = requests.get(
        url=f'{context.auth_url}/api/account/username?username={user}&clientId={organization}')
    if not response.ok:
        raise Exception({
            'status_code': response.status_code,
            'text': response.text
        })

    return response.json()


def is_user_available(context, user, organization):
    return is_user_available_response(context, user, organization)['isAvailable']
