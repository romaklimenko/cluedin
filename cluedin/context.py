import json
import requests
from .utils import parse_jwt_payload


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
    def from_dict(cls, d: dict):
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

        if 'domain' in d:
            domain = d['domain']

        if 'org_name' in d:
            org_name = d['org_name']
        elif 'organization' in d:
            org_name = d['organization']  # TODO: remove in 2.0.0

        if 'user_email' in d:
            user_email = d['user_email']
        elif 'user' in d:
            user_email = d['user']  # TODO: remove in 2.0.0

        if 'user_password' in d:
            user_password = d['user_password']
        elif 'password' in d:
            user_password = d['password']  # TODO: remove in 2.0.0

        if 'protocol' in d:
            protocol = d['protocol']
        else:
            protocol = 'https'

        if 'access_token' in d:
            access_token = d['access_token']

        if 'org_url' in d:
            org_url = d['org_url']

        if 'auth_url' in d:
            auth_url = d['auth_url']

        if 'api_url' in d:
            api_url = d['api_url']

        if 'gql_url' in d:
            gql_url = d['gql_url']

        if 'gql_api_url' in d:
            gql_api_url = d['gql_api_url']

        if 'public_api_url' in d:
            public_api_url = d['public_api_url']

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
        with open(file_path, 'r') as file:
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
            data=data)
        self.access_token = response.json()['access_token']
        self.jwt_payload = parse_jwt_payload(self.access_token)
