# CluedIn

[cluedin](https://pypi.org/project/cluedin/) is a Python client for [CluedIn](https://www.cluedin.com/) API.

## Installation

From [PyPi](https://pypi.org/project/cluedin/):

```shell
pip install cluedin
```

## Quick start

### CluedIn context configuration

Create a JSON file with context configuration to your CluedIn instance:

In this file, parameters have the following meaning:

- `protocol` - `http` if your CluedIn instance is not secured with a TLS certicate. Otherwise, `https` by default.
- `domain` – CluedIn instance domain without the Organization prefix.
- `org_name` – the name of Organization (a.k.a. Organization prefix).
- `user_email` – the user's email.
- `user_password` – the user's password.
- `verify_tls` – `false`, if an unknown CA signs the TLS certificate. Otherwise, `true` by default.

Here is an example of a file for a CluedIn instance running locally from a [Home](https://cluedin-io.github.io/Home/) repository:

```json
{
  "protocol": "http",
  "domain": "127.0.0.1.nip.io",
  "org_name": "foobar",
  "user_email": "admin@foobar.com",
  "user_password": "Foobar23!"
}
```

We add the protocol, but we can skip this parameter if the URL starts with `https`. Likewise, we can skip `verify_tls` because it only makes sense for HTTPs URLs.

Alternatively, to provide email and password, you can obtain an API access token from CluedIn UI and provide it in the file:

```json
{
  "protocol": "http",
  "domain": "127.0.0.1.nip.io",
  "org_name": "foobar",
  "access_token": "..."
}
```

When the configuration file exists, you can export its path to an environment variable:

```shell
export CLUEDIN_CONTEXT=~/.cluedin/home.json
```

Now, you can load this file from your Python code and get an access token (if not already provided):

```python
import cluedin

context = Context.from_json_file(os.environ['CLUEDIN_CONTEXT'])
context.get_token()
```

You could also do it without the context file:

```python
context = {
    "protocol": "http",
    "domain": "127.0.0.1.nip.io",
    "org_name": "foobar",
    "user_email": "admin@foobar.com",
    "user_password": "Foobar23!"
}

context = Context.from_dict(context)
context.get_token()
```

### GraphQL

Get entities:

```python
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
        }
      }
    }
"""

variables = {
    "query": "*",
    "pageSize": 10_000
}

# it's important to request cursor in your GraphQL query,
# so cluedin.gql.entries would be able to request and return all pages
entities = cluedin.gql.entries(context, query, variables):
```

## API

### Environment

- `CLUEDIN_REQUEST_TIMEOUT_IN_SECONDS` - CluedIn API request timeout (in seconds). If not set, then it defaults to `300` (5 minutes).

### Context

- `Context.from_dict(cls, context_dict: dict) -> Context` – creates a new `Context` object from a `dict`.
- `Context.from_json_file(file_path: str) -> Context` – creates a new `Context` object from a JSON-file.

### Account

- `cluedin.account.get_users(context: Context, org_id: str = None) -> list` – returns all users for Organization.
- `cluedin.account.is_organization_available_response(context: Context, org_name: str) -> dict` – checks if a given Organization name is available. This method returns a JSON-response serialized into a `dict`.
- `cluedin.account.is_organization_available(context: Context, org_name: str) -> bool` – checks if a given Organization name is available. Returns a Boolean.
- `cluedin.account.is_user_available_response(context: Context, user_email: str, org_name: str) -> dict` – checks, if a user with a given email can be created or this email is already reserved. This method returns a JSON-response serialized into a `dict`.
- `cluedin.account.is_user_available(context: Context, user_email: str, org_name: str) -> bool` – checks, if a user with a given email can be created or this email is already reserved. This method returns a JSON-response serialized into a `dict`. Returns a Boolean.
- `cluedin.account.get_invitation_code(context: Context, email: str) -> str` – returns an invitation code for a given email.
- `cluedin.account.create_organization(context: Context, user_email: str, password: str, org_name: str, org_sub_domain: str = None, email_domain: str = None, allow_email_domain_signup: bool = True, new_account_access_key: str = None) -> dict` - creates a new Organization. This method returns a JSON-response serialized into a `dict`.
- `cluedin.account.create_user(context: Context, user_email: str, user_password: str) -> requests.models.Response` – creates a new user. This method returns `requests.models.Response`.
- `cluedin.account.create_admin_user(context: Context, user_email: str, user_password: str) -> requests.models.Response` – creates a new admin user. This method returns `requests.models.Response`.
- `cluedin.account.get_user(context: Context, user_id: str = None) -> dict` – returns a user by ID. If `user_id` is nor provided, the current user is returned. This method returns a JSON-response serialized into a `dict`.

### Entity

- `cluedin.entity.get_entity_blob(context: Context, entity_id: str) -> str` – returns an entity blob by ID.
- `cluedin.entity.get_entity_as_clue(context: Context, entity_id: str) -> str` – returns an entity as a clue by ID.

### GraphQL

- `cluedin.gql.gql(context: Context, query: str, variables: dict = None) -> dict` – sends a GraphQL request and returns a response.
- `cluedin.gql.org_gql(context: Context, query: str, variables: dict = None) -> dict` – sends a GraphQL request to Organization endpoint and returns a response.
- `cluedin.gql.entries(context: Context, query: str, variables: dict = None, flat=False) -> list` – returns entries from a GraphQL search query. If cursor is requested in the GraphQL query (see the example above and tests), then it proceeds to next pages to return all results. If `flat` is `True`, then it flattens the `properties` dictionary of each returned entity.

### JSON

- `dump(file: str, obj: Any) -> None` – serialize obj as a JSON formatted stream to file.
- `load(file: str) -> Any` – deserialize file to a Python object.

### JWT

- `cluedin.jwt.get_jwt_payload(jwt: str) -> dict` – parses a JWT (JSON Web Token, a.k.a. access token or API token), and returns its payload serialized into a `dict`.

### Public API

- `cluedin.public.post_clue(context: Context, clue: str, content_type: str = 'application/xml') -> str` – posts a clue in XML or JSON format. This method returns an operation result as a string.
- `cluedin.public.restore_user_entities(context: Context) -> list` – if you accidentally deleted `/Infrastructure/User` entities, this method gets all users and restores entities for those who miss them.

### Vocabulary

- `cluedin.vocab.get_vocab_keys(context: Context) -> list` – gets all vocabulary keys.
