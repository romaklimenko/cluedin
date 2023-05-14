import os

from .ctx import cluedin


class TestContext:
    # pylint: disable=missing-docstring

    def test_from_json_file(self):

        # Act

        context = cluedin.Context.from_json_file(os.environ['CLUEDIN_CONTEXT'])

        # Assert

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
        #     "user_password": "Foobar23!"
        # }

        # Act

        context = cluedin.Context.from_json_file(os.environ['CLUEDIN_CONTEXT'])

        # Assert

        assert context.access_token is None

        context.get_token()

        assert context.access_token
        assert context.jwt_payload
        assert context.jwt_payload['OrganizationId']
