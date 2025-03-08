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

- `protocol` - `http` if your CluedIn instance is not secured with a TLS certificate. Otherwise, `https` by default.
- `domain` – CluedIn instance domain without the Organization prefix.
- `org_name` – the name of Organization (a.k.a. Organization prefix).
- `user_email` – the user's email.
- `user_password` – the user's password.
- `verify_tls` – `false`, if an unknown CA signs the TLS certificate. Otherwise, `true` by default.

Here is an example of a file for a CluedIn instance running locally from a [Home](https://cluedin-io.github.io/Home/) repository:

```json
{
  "domain": "mdm.saas-cluedin.com",
  "org_name": "foobar",
  "user_email": "admin@foobar.com",
  "user_password": "Foobar23!"
}
```

We add the `protocol`, but we can skip this parameter if the URL starts with `https`.
If you use self-signed certificates, you can add `verify_tls: false` to avoid certificate verification.

Alternatively, to provide email and password, you can obtain an API access token from CluedIn UI and provide it in the file:

```json
{
  "domain": "mdm.saas-cluedin.com",
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
context.get_token() # call it only if access_token is not provided in the context file
```

You could also do it without the context file:

```python
context = {
    "domain": "mdm.saas-cluedin.com",
    "org_name": "foobar",
    "user_email": "admin@foobar.com",
    "user_password": "Foobar23!"
}

context = Context.from_dict(context)
context.get_token()
```

Or, you can infer the context from the JWT token:

```python
context = Context.from_jwt(API_TOKEN)
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

- `cluedin.Context.from_dict(cls, context_dict: dict) -> Context` – creates a new `Context` object from a `dict`.
- `cluedin.Context.from_json_file(file_path: str) -> Context` – creates a new `Context` object from a JSON-file.
- `cluedin.Context.from_jwt(jwt: str) -> Context` – creates a new `Context` object from a JWT (JSON Web Token, a.k.a. access token or API token).

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

### Ingestion

- `cluedin.ingestion.post(context: Context, url: str, collection: list[Any], batch_size: int = 10_000, delay_in_seconds: int = 0) -> Generator` – posts data to CluedIn ingestion endpoint. This method splits the collection into batches and sends them to CluedIn. If `delay_in_seconds` is set, then it waits for this time before sending the next batch. Returns a generator of responses.

### GraphQL

- `cluedin.gql.gql(context: Context, query: str, variables: dict = None) -> dict` – sends a GraphQL request and returns a response.
- `cluedin.gql.org_gql(context: Context, query: str, variables: dict = None) -> dict` – sends a GraphQL request to Organization endpoint and returns a response.
- `cluedin.gql.entries(context: Context, query: str, variables: dict = None, flat=False) -> Generator` – returns entries from a GraphQL search query. If cursor is requested in the GraphQL query (see the example above and tests), then it proceeds to next pages to return all results. If `flat` is `True`, then it flattens the `properties` dictionary of each returned entity.
- `search(context: Context, search_query: str, page_size: int = 10_000) -> Generator` – returns entities by a search query. This method is a wrapper around `cluedin.gql.entries`.

### JSON

- `cluedin.json.dump(file: str, obj: Any) -> None` – serialize obj as a JSON formatted stream to file.
- `cluedin.json.load(file: str) -> Any` – deserialize file to a Python object.

### JWT

- `cluedin.jwt.get_jwt_payload(jwt: str) -> dict` – parses a JWT (JSON Web Token, a.k.a. access token or API token), and returns its payload serialized into a `dict`.

### Public API

- `cluedin.public.post_clue(context: Context, clue: str, content_type: str = 'application/xml') -> str` – posts a clue in XML or JSON format. This method returns an operation result as a string.
- `cluedin.public.restore_user_entities(context: Context) -> list` – if you accidentally deleted `/Infrastructure/User` entities, this method gets all users and restores entities for those who miss them.

### Rules

- `cluedin.rules.RuleScope` - an enumeration of rule scopes: `DATA_PART`, `ENTITY`, `SURVIVORSHIP`.
- `cluedin.rules.get_rules(context: Context, scope=RuleScope.DATA_PART) -> dict` – returns all rules for a given scope. This method returns a JSON-response serialized into a `dict`.
- `cluedin.rules.get_rule(context: Context, rule_id: str) -> dict` – returns a rule by ID. This method returns a JSON-response serialized into a `dict`.

#### Evaluator

- `cluedin.rules.evaluator.default_get_property_name(field: str) -> str` – returns a default property name for a given field. Used to map CluedIn Rules fields to your fields.
- `cluedin.rules.evaluator.default_get_value(field: str, obj: dict) -> Any` – returns a default value for a given field. Used to map CluedIn Rules fields to your fields.
- `cluedin.rules.Evaluator` – a class to evaluate CluedIn Rules.
- `cluedin.rules.Evaluator.evaluate(context: Context, rule: dict, obj: dict) -> bool` – evaluates a rule for an object. Returns a Boolean:

  - `cluedin.rules.get_matching_objects(self, objects) -> list` – returns a list of objects that match the rule.
  - `cluedin.rules.object_matches_rules(self, obj) -> bool` – returns `True` if an object matches the rule.
  - `cluedin.rules.explain(self) -> str` – returns an explanation of the rule (in pandas `DataFrame.query` terms).

#### Operators

- `cluedin.rules.operators.default_get_operator(operator_id) -> Any` – returns a default operator for a given operator ID. Used to map CluedIn Rules operators to your operators.

You can add custom operations (see `test_operators.py` for examples), but the following CluedIn Rules operators are supported out of the box:

- `Is Not True`
- `Is True`
- `Begins With`
- `Between`
- `Contains`
- `Ends With`
- `Equals`
- `Exists`
- `Greater`
- `Greater or Equal`
- `In`
- `Is False`
- `Is Not Null`
- `Is Null`
- `Is True`
- `Less`
- `Less or Equal`
- `Matches pattern`
- `Not Begins With`
- `Not Between`
- `Not Contains`
- `Not Ends With`
- `Not Equal`
- `Does Not Exist`
- `Not In`
- `Does not match pattern`

### Vocabulary

- `cluedin.vocab.get_vocab_keys(context: Context) -> list` – gets all vocabulary keys.
