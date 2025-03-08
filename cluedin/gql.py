from typing import Any, Generator

import requests

from .context import Context
from .env import CLUEDIN_REQUEST_TIMEOUT_IN_SECONDS


def gql(context: Context, query: str, variables: dict = None) -> dict:
    """Send a GraphQL query to CluedIn.

    Args:
        context (Context): Context object.
        query (str): GraphQL query.
        variables (dict, optional): A dictionary of variables to be used in the query.
            Defaults to {}.

    Returns:
        dict: JSON response.
    """
    headers = {
        'Authorization': f'Bearer {context.access_token}'
    }

    if variables is None:
        variables = {}

    json = {
        'query': query,
        'variables': variables
    }

    response = requests.post(
        url=context.gql_api_url,
        json=json,
        headers=headers,
        timeout=CLUEDIN_REQUEST_TIMEOUT_IN_SECONDS,
        verify=context.verify_tls
    )

    response.raise_for_status()

    return response.json()


def org_gql(context: Context, query: str, variables: dict = None) -> dict:
    """Send a GraphQL query to CluedIn Organization endpoint.

    Args:
        context (Context): Context object.
        query (str): GraphQL query.
        variables (dict, optional): A dictionary of variables to be used in the query.
            Defaults to {}.

    Returns:
        dict: JSON response.
    """
    headers = {
        'Authorization': f'Bearer {context.access_token}'
    }

    if variables is None:
        variables = {}

    json = {
        'query': query,
        'variables': variables
    }

    response = requests.post(
        url=context.gql_org_url,
        json=json,
        headers=headers,
        timeout=CLUEDIN_REQUEST_TIMEOUT_IN_SECONDS,
        verify=context.verify_tls
    )

    response.raise_for_status()

    return response.json()


def entries(context: Context, query: str, variables: dict = None, flat=False) \
        -> Generator[Any, Any, Any]:
    """Get entries from a GraphQL query. This function is a generator.
        It uses the cursor to get the next page of entries.

    Args:
        context (Context): Context object.
        query (str): GraphQL query.
        variables (dict, optional): A dictionary of variables to be used in the query.
        flat (bool, optional): Flatten the properties. Defaults to False.

    Returns:
        Generator[Any, Any, Any]: Iterator of entries.
    """

    def flatten_properties(d):
        if 'properties' not in d:
            return d

        for k, v in d['properties'].items():
            if k == 'attribute-type':
                continue

            if k.startswith('property-'):
                k = k[9:]  # len('property-') == 9

            d[k] = v

        del d['properties']

        return d

    if variables is None:
        variables = {}

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
            if flat:
                entry = flatten_properties(entry)
            yield entry

        variables['cursor'] = cursor

        response = gql(context, query, variables)


def search(context: Context, search_query: str, page_size: int = 10_000) -> Generator[Any, Any, Any]:
    """
    Search for entities in CluedIn.

    Args:
        context (Context): Context object.
        search_query (str): Search query.
        page_size (int, optional): Page size. Defaults to 10_000.

    Returns:
        Generator[Any, Any, Any]: Iterator of entities.
    """
    query = """
query searchEntities($cursor: PagingCursor, $query: String, $pageSize: Int) {
  search(
    query: $query
    cursor: $cursor
    pageSize: $pageSize
    sort: FIELDS
    sortFields: {field: "id", direction: ASCENDING}
  ) {
    totalResults
    cursor
    entries {
      id
      name
      displayName
      description
      discoveryDate
      createdDate
      modifiedDate
      lastProcessedDate
      entityType
      originEntityCode
      codes
      tags
      properties
    }
  }
}
    """

    variables = {'query': search_query, 'pageSize': page_size}

    for entity in entries(context, query, variables=variables, flat=True):
        yield entity
