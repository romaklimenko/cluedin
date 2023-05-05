from cluedin import load_token_into_context


class TestAuth:
    def test_load_token_into_context(self):
        context = {
            "protocol": "http", # default - `https`
            "domain": "cluedin.local",
            "organization": "foobar",
            "user": "admin@foobar.com",
            "password": "Foobar23!"
        }

        assert 'access_token' not in context

        load_token_into_context(context)

        assert len(context['access_token']) > 0
