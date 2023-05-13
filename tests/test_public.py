import os
from .ctx import cluedin
from cluedin import Context


class TestPublic:
    def test_restore_user_entities(self):

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
