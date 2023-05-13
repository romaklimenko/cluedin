import os
import pytest
import requests
from .ctx import cluedin
from cluedin import Context


class TestGql:
    def test_gql(self):
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
            "pageSize": 1
        }

        response = cluedin.gql.gql(context, query, variables)

        assert 'data' in response
        assert 'search' in response['data']
        assert 'cursor' in response['data']['search']
        assert 'entries' in response['data']['search']

    def test_gql_error(self):
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

        with pytest.raises(requests.HTTPError) as exception:
            cluedin.gql.gql(context, query, variables)

        assert str(exception.value) == "{'status_code': 400, 'text': ''}"

    def test_entries(self):
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
            "pageSize": 5
        }

        entries = []

        for entry in cluedin.gql.entries(context, query, variables):
            entries.append(entry)
            assert 'id' in entry
            assert 'name' in entry
            assert 'entityType' in entry

        assert len(entries) > 0

    def test_actions(self):
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
            "pageSize": 5
        }

        entries = []

        for entry in cluedin.gql.entries(context, query, variables):
            entries.append(entry)
            assert 'id' in entry
            assert 'name' in entry
            assert 'entityType' in entry

        assert len(entries) > 0
