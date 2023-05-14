import os

# pylint: disable=wrong-import-order
from .ctx import cluedin
from cluedin import Context


class TestAccount:
    # pylint: disable=missing-docstring

    # Account

    def test_get_users(self):
        # Arrange
        context = Context.from_json_file(os.environ['CLUEDIN_CONTEXT'])
        context.get_token()

        # Act and Assert

        # get users without providing organization_id

        users = cluedin.account.get_users(context)
        organization_id = users[0]['Account']['OrganizationId']

        assert len(users) > 0

        # get users by organization_id

        users = cluedin.account.get_users(context, organization_id)

        assert len(users) > 0

    # Availability

    def test_is_organization_available(self):

        # Arrange

        context = Context.from_json_file(os.environ['CLUEDIN_CONTEXT'])
        context.get_token()

        # Act and Assert

        assert not cluedin.account.is_organization_available(
            context, context.org_name)

        assert cluedin.account.is_organization_available(context, 'foobaz')

    def test_is_user_available(self):

        # Arrange

        context = Context.from_json_file(os.environ['CLUEDIN_CONTEXT'])
        context.get_token()

        # Act and Assert

        assert not cluedin.account.is_user_available(
            context, context.user_email, context.org_name)

        assert cluedin.account.is_user_available(
            context, 'admin@foobaz.com', context.org_name)
