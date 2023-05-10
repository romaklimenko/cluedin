import os
import cluedin


class TestAuth:
    def test_load_token_into_context(self):
        # context = {
        #     "protocol": "http", # default - `https`
        #     "domain": "cluedin.local",
        #     "organization": "foobar",
        #     "user": "admin@foobar.com",
        #     "password": "Foobar23!"
        # }

        context = cluedin.utils.load(os.environ['CLUEDIN_CONTEXT'])

        assert 'access_token' not in context

        cluedin.load_token_into_context(context)

        assert len(context['access_token']) > 0
        assert context['jwt'] is not None
        assert context['jwt']['OrganizationId'] is not None
