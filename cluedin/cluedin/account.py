import requests
from .urls import get_auth_url


def is_organization_available_response(context, organization):
    headers = {
        'Authorization': 'Bearer {}'.format(context['access_token'])
    }
    response = requests.get(
        url=f'{get_auth_url(context)}/api/account/available?clientId={organization}',
        headers=headers)

    if not response.ok:
        raise Exception({
            'status_code': response.status_code,
            'text': response.text
        })

    return response.json()


def is_organization_available(context, organization):
    return is_organization_available_response(context, organization)['isAvailable']


def is_user_available_response(context, user, organization):
    response = requests.get(
        url=f'{get_auth_url(context)}/api/account/username?username={user}&clientId={organization}')
    if not response.ok:
        raise Exception({
            'status_code': response.status_code,
            'text': response.text
        })

    return response.json()


def is_user_available(context, user, organization):
    return is_user_available_response(context, user, organization)['isAvailable']
