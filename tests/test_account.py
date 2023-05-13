import os
from .ctx import cluedin
from cluedin import Context


class TestAccount:

    # Account

    def test_get_users(self):
        context = Context.from_json_file(os.environ['CLUEDIN_CONTEXT'])
        context.get_token()

        # get users without providing organization_id

        users = cluedin.account.get_users(context)
        organization_id = users[0]['Account']['OrganizationId']

        assert len(users) > 0

        # get users by organization_id

        users = cluedin.account.get_users(context, organization_id)

        assert len(users) > 0

    # Availability

    def test_is_organization_available(self):
        context = Context.from_json_file(os.environ['CLUEDIN_CONTEXT'])
        context.get_token()

        assert not cluedin.account.is_organization_available(context, 'foobar')

        assert cluedin.account.is_organization_available(context, 'foobaz')

    def test_is_user_available(self):
        context = Context.from_json_file(os.environ['CLUEDIN_CONTEXT'])
        context.get_token()

        assert not cluedin.account.is_user_available(
            context, 'admin@foobar.com', 'foobar')

        assert cluedin.account.is_user_available(
            context, 'admin@foobaz.com', 'foobar')
