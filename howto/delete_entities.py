import time
from datetime import timedelta

import cluedin

ctx = cluedin.Context.from_json_file('.cluedin/sandbox.json')
ctx.get_token()

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
    "query": "entityType:/IMDb/Person",
    "pageSize": 10_000
}

start = time.time()
iteration_start = start

for i, entity in enumerate(cluedin.gql.entries(context=ctx, query=query, variables=variables)):
    # print(entity['id'], entity['name'], entity['entityType'])
    if i % 10_000 == 0:
        time_from_start = timedelta(seconds=time.time() - start)
        time_from_iteration_start = timedelta(seconds=time.time() - iteration_start)
        iteration_start = time.time()
        print(
            f'{time_from_start} {time_from_iteration_start}: {i} entities queued for deletion')
