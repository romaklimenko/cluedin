import requests
from .urls import get_graphql_url


def gql(context, query, variables={}):
    headers = {
        'Authorization': 'Bearer {}'.format(context['access_token'])
    }
    json = {
        'query': query,
        'variables': variables
    }
    response = requests.post(
        url=get_graphql_url(context),
        json=json,
        headers=headers
    )

    if not response.ok:
        raise Exception({
            'status_code': response.status_code,
            'text': response.text
        })

    return response.json()


def entries(context, query, variables):
    response = gql(context, query, variables)
    while ('data' in response and
           'search' in response['data'] and
           'cursor' in response['data']['search'] and
            'entries' in response['data']['search']):
        cursor = response['data']['search']['cursor']
        entries = response['data']['search']['entries']
        if len(entries) == 0:
            return
        for entry in entries:
            yield entry
        variables['cursor'] = cursor
        response = gql(context, query, variables)
