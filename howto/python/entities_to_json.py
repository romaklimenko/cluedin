import json

import cluedin
from cluedin import Context

context_data = {
    "protocol": "http",  # default - `https`
    "domain": "cluedin.local:8888",
    "org_name": "foobar",
    "user_email": "admin@foobar.com",
    "user_password": "Foobar23!"
}

context = Context.from_dict(context_data)
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
        }
      }
    }
"""

variables = {
    "query": "entityType:/Duck",
    "pageSize": 10_000
}

entities = list(cluedin.gql.entries(context, query, variables))


def key(x):
    if 'name' not in x or x['name'] is None:
        return ''
    else:
        return str(x['name'])


sorted_entities = sorted(entities, key=key)

with open('entities.json', 'w', encoding='utf-8') as file:
    json.dump(sorted_entities, file, ensure_ascii=False,
              indent=2, sort_keys=False)
