# CluedIn

[cluedin](https://pypi.org/project/cluedin/) is a Python client for [CluedIn](https://www.cluedin.com/) API. It can help you with the following:

* getting JWT access tokens to CluedIn
* calling CluedIn REST API
* calling CluedIn GraphQL API

The use is pretty simple. First, install it from [PyPi](https://pypi.org/project/cluedin/):
```shell
pip install cluedin
```

Next, you will need to obtain an access token:
```python
import cluedin

context = {
    "protocol": "http", # if you skip this parameter, it will fall back to `https`
    "domain": "cluedin.local",
    "organization": "foobar",
    "user": "admin@foobar.com",
    "password": "Foobar23!"
}

cluedin.load_token_into_context(context)

print(context['access_token'])
```


Run a GraphQL query:
```python
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
```

Get paged results:
```python
import numpy as np
import pandas as pd

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
    "pageSize": 10000
}

entries = np.array([x for x in cluedin.gql.entries(context, query, variables)])

df = pd.DataFrame(entries.tolist(), columns=list(entries[0].keys()))
```

To be continued...
