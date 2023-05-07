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
