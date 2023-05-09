import os
import cluedin


class TestAccount:
    def test_is_organization_available(self):
        context = cluedin.utils.load(os.environ['CLUEDIN_CONTEXT'])
        cluedin.load_token_into_context(context)

        assert not cluedin.account.is_organization_available(context, 'foobar')

        assert cluedin.account.is_organization_available(context, 'foobaz')

    def test_is_user_available(self):
        context = cluedin.utils.load(os.environ['CLUEDIN_CONTEXT'])
        cluedin.load_token_into_context(context)

        assert not cluedin.account.is_user_available(
            context, 'admin@foobar.com', 'foobar')

        assert cluedin.account.is_user_available(
            context, 'admin@foobaz.com', 'foobar')
