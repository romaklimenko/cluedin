import requests
from .context import Context
from . import CLUEDIN_REQUEST_TIMEOUT


def gql(context: Context, query: str, variables: dict = {}) -> str:
    headers = {
        'Authorization': f'Bearer {context.access_token}'
    }
    json = {
        'query': query,
        'variables': variables
    }
    response = requests.post(
        url=context.gql_api_url,
        json=json,
        headers=headers,
        timeout=CLUEDIN_REQUEST_TIMEOUT
    )

    if not response.ok:
        response.raise_for_status()

    return response.json()


def entries(context: Context, query: str, variables: dict = {}) -> list:
    response = gql(context, query, variables)
    while ('data' in response and
           'search' in response['data'] and
           'cursor' in response['data']['search'] and
            'entries' in response['data']['search']):
        cursor = response['data']['search']['cursor']
        page_entries = response['data']['search']['entries']
        if len(page_entries) == 0:
            return
        for entry in page_entries:
            yield entry
        variables['cursor'] = cursor
        response = gql(context, query, variables)
