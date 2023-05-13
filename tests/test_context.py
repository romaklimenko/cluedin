import os
from .ctx import cluedin


class TestContext:
    def test_from_json_file(self):

        context = cluedin.Context.from_json_file(os.environ['CLUEDIN_CONTEXT'])

        assert context.domain
        assert context.org_name
        assert context.user_email
        assert context.user_password
        assert context.protocol
        assert context.access_token is None

    def test_get_token(self):
        # {
        #     "protocol": "http", # default - `https`
        #     "domain": "cluedin.local",
        #     "org_name": "foobar",
        #     "user_email": "admin@foobar.com",
        #     "password": "Foobar23!"
        # }

        context = cluedin.Context.from_json_file(os.environ['CLUEDIN_CONTEXT'])

        assert context.access_token is None

        context.get_token()

        assert context.access_token
        assert context.jwt_payload
        assert context.jwt_payload['OrganizationId']
