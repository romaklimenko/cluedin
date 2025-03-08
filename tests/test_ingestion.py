import os

import pytest

from cluedin import Context

# pylint: disable=wrong-import-order
from .ctx import cluedin


class TestIngestion:
    # pylint: disable=missing-docstring

    @pytest.mark.integration
    def test_post(self):
        # Arrange
        context = Context.from_json_file(os.environ['CLUEDIN_CONTEXT'])
        # For this test, the context must have access_token (API token).
        # context.get_token()

        data = []
        for i in range(100_000):
            data.append({
                'id': i,
                'name': f'User {i}',
                'email': f'user{i}@cluedin.com'
            })

        responses = []

        # Act

        for response in cluedin.ingestion.post(
                context,
                os.environ['CLUEDIN_INGESTION_URL'],
                data):
            responses.append(response)

        # Assert

        assert len(responses) == 10
        assert all('payload' in response for response in responses)
        assert all('response' in response for response in responses)
        assert all(len(response['payload']) ==
                   10_000 for response in responses)
