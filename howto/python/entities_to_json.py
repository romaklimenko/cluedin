import os
import cluedin
from cluedin import Context

context = cluedin.from_json_file(os.environ['CLUEDIN_CONTEXT'])
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
    "query": "entityType:/Person",
    "pageSize": 10_000
}

entities = list(cluedin.gql.entries(context, query, variables))


def key(x):
    if 'name' not in x or x['name'] is None:
        return ''
    else:
        return str(x['name'])


sorted_entities = sorted(entities, key=key)

cluedin.utils.save(sorted_entities, 'entities.json', sort_keys=False)
