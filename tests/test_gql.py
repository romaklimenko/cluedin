import os

import pytest
import requests

# pylint: disable=wrong-import-order
from .ctx import cluedin
from cluedin import Context


class TestGql:
    # pylint: disable=missing-docstring

    def test_gql(self):

        # Arrange
        context = Context.from_json_file(os.environ['CLUEDIN_CONTEXT'])
        context.get_token()

        query = """
            query searchEntities($cursor: PagingCursor, $query: String, $pageSize: Int) {
              search(query: $query, sort: DATE, cursor: $cursor, pageSize: $pageSize) {
                totalResults
                cursor
                entries {
                  id
                  name
                  entityType
                }
              }
            }
        """

        variables = {
            "query": "entityType:/Infrastructure/User",
            "pageSize": 10_000
        }

        # Act

        response = cluedin.gql.gql(context, query, variables)

        assert 'data' in response
        assert 'search' in response['data']
        assert 'cursor' in response['data']['search']
        assert 'entries' in response['data']['search']

    def test_gql_error(self):

        # Arrange

        context = Context.from_json_file(os.environ['CLUEDIN_CONTEXT'])
        context.get_token()

        query = """
            query searchEntities($cursor: PagingCursor, $query: String, $pageSize: Int) {
              search(query: $query, sort: DATE, cursor: $cursor, pageSize: $pageSize) {
                totalResults
                cursor
                entries {
                  id
                  name
                  entityType
                }
              }
            }
        """

        variables = {
            "query": "entityType:/Infrastructure/User",
            "pageSize": 1,
            "cursor": ""  # this will break the response
        }

        # Act and Assert

        with pytest.raises(requests.HTTPError) as exception:
            cluedin.gql.gql(context, query, variables)

        # Assert

        assert str(exception.value).startswith(
            '400 Client Error: Bad Request for url:')

    def test_org_gql(self):

        # Arrange
        context = Context.from_json_file(os.environ['CLUEDIN_CONTEXT'])
        context.get_token()

        query = """
            {
              notification {
                serverStatus
                __typename
              }
            }
        """

        variables = { }

        # Act

        response = cluedin.gql.org_gql(context, query, variables)

        assert 'data' in response
        assert 'notification' in response['data']
        assert 'serverStatus' in response['data']['notification']
        assert 'server' in response['data']['notification']['serverStatus']
        assert 'dataSource' in response['data']['notification']['serverStatus']
        assert 'mapping' in response['data']['notification']['serverStatus']
        assert 'prepare' in response['data']['notification']['serverStatus']

    def test_entries(self):

        # Arrange

        context = Context.from_json_file(os.environ['CLUEDIN_CONTEXT'])
        context.get_token()

        query = """
            query searchEntities($cursor: PagingCursor, $query: String, $pageSize: Int) {
              search(query: $query, sort: DATE, cursor: $cursor, pageSize: $pageSize) {
                totalResults
                cursor
                entries {
                  id
                  name
                  entityType
                }
              }
            }
        """

        variables = {
            "query": "*",
            "pageSize": 10_000
        }

        entries = []

        # Act and Assert

        for entry in cluedin.gql.entries(context, query, variables):
            entries.append(entry)
            assert 'id' in entry
            assert 'name' in entry
            assert 'entityType' in entry

        assert len(entries) > 0

    def test_actions(self):

        # Arrange

        context = Context.from_json_file(os.environ['CLUEDIN_CONTEXT'])
        context.get_token()

        query = """
            query searchEntities($cursor: PagingCursor, $query: String, $pageSize: Int) {
              search(query: $query, sort: DATE, cursor: $cursor, pageSize: $pageSize) {
                totalResults
                cursor
                entries {
                  id
                  name
                  entityType
                  actions {
                    postProcess
                  }
                }
              }
            }
        """

        variables = {
            "query": "entityType:/Infrastructure/User",
            "pageSize": 10_000
        }

        entries = []

        # Act and Assert

        for entry in cluedin.gql.entries(context, query, variables):
            entries.append(entry)
            assert 'id' in entry
            assert 'name' in entry
            assert 'entityType' in entry

        assert len(entries) > 0
