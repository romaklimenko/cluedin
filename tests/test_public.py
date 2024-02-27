import os

import pytest

# pylint: disable=wrong-import-order
from .ctx import cluedin
from cluedin import Context


class TestPublic:
    # pylint: disable=missing-docstring

    @pytest.mark.integration
    def test_restore_user_entities(self):

        # Arrange

        context = Context.from_json_file(os.environ['CLUEDIN_CONTEXT'])
        context.get_token()

        query = """
            query searchEntities($cursor: PagingCursor, $query: String, $pageSize: Int) {
              search(
                query: $query,
                sort: FIELDS,
                cursor: $cursor,
                pageSize: $pageSize
                sortFields: {field: "id", direction: ASCENDING}
              ) {
                totalResults
                cursor
                entries {
                  id
                  name
                  entityType
                  actions {
                    deleteEntity
                  }
                }
              }
            }
        """

        variables = {
            "query": "entityType:/Infrastructure/User +name:rok@cluedin.com",
            "pageSize": 1
        }

        cluedin.gql.gql(context, query, variables)

        # Act

        results = cluedin.public.restore_user_entities(context)

        # Assert
        assert len(results) == 1
