import json
import requests
from .jwt import get_jwt_payload
from .env import CLUEDIN_REQUEST_TIMEOUT


class Context:
    def __init__(self,
                 domain: str,
                 org_name: str,
                 user_email: str,
                 user_password: str,
                 protocol: str = 'https',
                 access_token: str = None,
                 org_url: str = None,
                 auth_url: str = None,
                 api_url: str = None,
                 gql_url: str = None,
                 gql_api_url: str = None,
                 public_api_url: str = None) -> None:
        self.domain = domain
        self.org_name = org_name
        self.user_email = user_email
        self.user_password = user_password
        self.protocol = protocol
        self.access_token = access_token
        if access_token:
            self.jwt_payload = parse_jwt_payload(access_token)

        if org_url is None:
            self.org_url = f'{self.protocol}://{self.org_name}.{self.domain}'
        else:
            self.org_url = org_url

        if auth_url is None:
            self.auth_url = f'{self.org_url}/auth'
        else:
            self.auth_url = auth_url

        if api_url is None:
            self.api_url = f'{self.org_url}/api/api'
        else:
            self.api_url = api_url

        if gql_url is None:
            self.gql_url = f'{self.org_url}/graphql'
        else:
            self.gql_url = gql_url

        if gql_api_url is None:
            self.gql_api_url = f'{self.api_url}/graphql'
        else:
            self.gql_api_url = gql_api_url

        if public_api_url is None:
            self.public_api_url = f'{self.org_url}/public/api'
        else:
            self.public_api_url = public_api_url

    @classmethod
    def from_dict(cls, context_dict: dict):
        domain: str = None
        org_name: str = None
        user_email: str = None
        user_password: str = None
        protocol: str = None
        access_token: str = None
        org_url: str = None
        auth_url: str = None
        api_url: str = None
        gql_url: str = None
        gql_api_url: str = None
        public_api_url: str = None

        if 'domain' in context_dict:
            domain = context_dict['domain']

        if 'org_name' in context_dict:
            org_name = context_dict['org_name']

        if 'user_email' in context_dict:
            user_email = context_dict['user_email']

        if 'user_password' in context_dict:
            user_password = context_dict['user_password']

        if 'protocol' in context_dict:
            protocol = context_dict['protocol']
        else:
            protocol = 'https'

        if 'access_token' in context_dict:
            access_token = context_dict['access_token']

        if 'org_url' in context_dict:
            org_url = context_dict['org_url']

        if 'auth_url' in context_dict:
            auth_url = context_dict['auth_url']

        if 'api_url' in context_dict:
            api_url = context_dict['api_url']

        if 'gql_url' in context_dict:
            gql_url = context_dict['gql_url']

        if 'gql_api_url' in context_dict:
            gql_api_url = context_dict['gql_api_url']

        if 'public_api_url' in context_dict:
            public_api_url = context_dict['public_api_url']

        return cls(protocol=protocol,
                   domain=domain,
                   org_name=org_name,
                   user_email=user_email,
                   user_password=user_password,
                   access_token=access_token,
                   org_url=org_url,
                   auth_url=auth_url,
                   api_url=api_url,
                   gql_url=gql_url,
                   gql_api_url=gql_api_url,
                   public_api_url=public_api_url)

    @staticmethod
    def from_json_file(file_path: str):
        with open(file_path, 'r', encoding='utf-8') as file:
            return Context.from_dict(json.load(file))

    def get_token(self) -> dict:
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {
            'username': self.user_email,
            'password': self.user_password,
            'client_id': self.org_name,
            'grant_type': 'password'
        }
        response = requests.post(
            url=f'{self.auth_url}/connect/token',
            headers=headers,
            data=data,
            timeout=CLUEDIN_REQUEST_TIMEOUT)
        self.access_token = response.json()['access_token']
        self.jwt_payload = get_jwt_payload(self.access_token)
