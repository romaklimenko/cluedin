import os

import pytest

from .ctx import cluedin


class TestContext:
    # pylint: disable=missing-docstring

    def test_from_json_file(self):

        # Act

        context = cluedin.Context.from_json_file("tests/fixtures/context.json")

        # Assert

        assert context.domain == "cluedin.local:8888"
        assert context.org_name == "foobar"
        assert context.user_email == "admin@foobar.com"
        assert context.user_password == "Foobar23!"
        assert context.protocol == "http"
        assert context.access_token is None

    @pytest.mark.integration
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
