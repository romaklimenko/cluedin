import json
from typing import Optional
from urllib.parse import urlparse

import requests

from .env import CLUEDIN_REQUEST_TIMEOUT_IN_SECONDS
from .jwt import get_jwt_payload


class Context:
    """Context object. Used to store information about the CluedIn instance."""

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
                 gql_org_url: str = None,
                 gql_api_url: str = None,
                 public_api_url: str = None,
                 verify_tls: bool = True) -> None:
        self.domain = domain
        self.org_name = org_name
        self.user_email = user_email
        self.user_password = user_password
        self.protocol = protocol
        self.access_token = access_token
        if access_token:
            self.jwt_payload = get_jwt_payload(access_token)

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

        if gql_org_url is None:
            self.gql_org_url = f'{self.org_url}/graphql'
        else:
            self.gql_org_url = gql_org_url

        if gql_api_url is None:
            self.gql_api_url = f'{self.api_url}/graphql'
        else:
            self.gql_api_url = gql_api_url

        if public_api_url is None:
            self.public_api_url = f'{self.org_url}/public/api'
        else:
            self.public_api_url = public_api_url

        self.verify_tls = verify_tls

    @classmethod
    def from_dict(cls, context_dict: dict):
        """Create a Context object from a dictionary.

        Args:
            context_dict (dict): Dictionary containing the context information.

        Returns:
            Context: Context object.
        """
        domain: Optional[str] = None
        org_name: Optional[str] = None
        user_email: Optional[str] = None
        user_password: Optional[str] = None
        protocol: str = 'https'
        access_token: Optional[str] = None
        org_url: Optional[str] = None
        auth_url: Optional[str] = None
        api_url: Optional[str] = None
        gql_org_url: Optional[str] = None
        gql_api_url: Optional[str] = None
        public_api_url: Optional[str] = None
        verify_tls: bool = True

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

        if 'access_token' in context_dict:
            access_token = context_dict['access_token']

        if 'org_url' in context_dict:
            org_url = context_dict['org_url']

        if 'auth_url' in context_dict:
            auth_url = context_dict['auth_url']

        if 'api_url' in context_dict:
            api_url = context_dict['api_url']

        # TODO: Remove in v3.0.0
        if 'gql_url' in context_dict:
            gql_org_url = context_dict['gql_url']

        if 'gql_org_url' in context_dict:
            gql_org_url = context_dict['gql_org_url']

        if 'gql_api_url' in context_dict:
            gql_api_url = context_dict['gql_api_url']

        if 'public_api_url' in context_dict:
            public_api_url = context_dict['public_api_url']

        if 'verify_tls' in context_dict:
            verify_tls = str(context_dict['verify_tls']).lower() == 'true'

        return cls(protocol=protocol,
                   domain=domain,
                   org_name=org_name,
                   user_email=user_email,
                   user_password=user_password,
                   access_token=access_token,
                   org_url=org_url,
                   auth_url=auth_url,
                   api_url=api_url,
                   gql_org_url=gql_org_url,
                   gql_api_url=gql_api_url,
                   public_api_url=public_api_url,
                   verify_tls=verify_tls)

    @staticmethod
    def from_json_file(file_path: str):
        """Create a Context object from a JSON file.

        Args:
            file_path (str): Path to the JSON file.

        Returns:
            Context: Context object.
        """
        with open(file_path, 'r', encoding='utf-8') as file:
            return Context.from_dict(json.load(file))

    @staticmethod
    def from_jwt(jwt: str):
        """Create a Context object from a JWT.

        Args:
            jwt (str): JWT.

        Returns:
            Context: Context object.
        """
        payload = get_jwt_payload(jwt)
        url = urlparse(payload['iss'])
        return Context.from_dict({
            'protocol': url.scheme,
            'domain': '.'.join(url.hostname.split('.')[1:]),
            'org_name': payload['ClientId'],
            'access_token': jwt
        })

    def get_token(self) -> dict:
        """Get a new access token from the CluedIn instance.

        Returns:
            dict: Dictionary containing the access token.
        """
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
            timeout=CLUEDIN_REQUEST_TIMEOUT_IN_SECONDS,
            verify=self.verify_tls)

        response.raise_for_status()

        response_json = response.json()

        self.access_token = response_json['access_token']
        self.jwt_payload = get_jwt_payload(self.access_token)

        return response_json

    def __repr__(self) -> str:
        password = '**********' if self.user_password else None
        access_token = '**********' if self.access_token else None
        return f"""Context:
    Domain: {self.domain}
    Organization Name: {self.org_name}
    User Email: {self.user_email}
    User Password: {password}
    Protocol: {self.protocol}
    Access Token: {access_token}
    Organization URL: {self.org_url}
    Authentication URL: {self.auth_url}
    API URL: {self.api_url}
    GQL Organization URL: {self.gql_org_url}
    GQL API URL: {self.gql_api_url}
    Public API URL: {self.public_api_url}
    Verify TLS: {self.verify_tls}
"""

    def __str__(self) -> str:
        return self.__repr__()
