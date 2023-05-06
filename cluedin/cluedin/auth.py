import requests
from .urls import get_auth_url


def get_token_response(context):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'username': context['user'],
        'password': context['password'],
        'client_id': context['organization'],
        'grant_type': 'password'
    }
    response = requests.post(
        url=f'{get_auth_url(context)}/connect/token',
        headers=headers,
        data=data)
    return response.json()


def load_token_into_context(context):
    token_response = get_token_response(context)
    context['access_token'] = token_response['access_token']
    return context
