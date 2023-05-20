import os
import random

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

    def test_get_invitation_code(self):

        # Arrange

        context = Context.from_json_file(os.environ['CLUEDIN_CONTEXT'])
        context.get_token()

        # Act

        invitation_code = cluedin.account.get_invitation_code(
            context, email=context.user_email)

        # Assert

        assert invitation_code == 'DE1703F42AA9E52B77F4D4EC2324581E'

    def test_create_organization(self):

        # Arrange

        context = Context.from_json_file(os.environ['CLUEDIN_CONTEXT'])
        context.get_token()

        # Act

        org_name = context.org_name + str(random.randint(1, 1000000))

        response = cluedin.account.create_organization(
            context,
            user_email=context.user_email,
            password=context.user_password,
            org_name=org_name,
            email_domain=context.user_email.split('@')[1],
            new_account_access_key=os.environ['CLUEDIN_NEW_ACCOUNT_ACCESS_KEY'])

        # Assert

        assert response is not None
        assert response['Active']
        assert response['ApplicationSubDomain'] == org_name
        assert response['EmailDomainName'] == context.user_email.split('@')[1]
        assert response['IsEmailDomainSignupActivated']
        assert response['Name'] == org_name

    def test_create_user(self):

        # Arrange

        context = Context.from_json_file(os.environ['CLUEDIN_CONTEXT'])
        context.get_token()

        user_email = f'testuser_{random.randint(1, 1000000)}@' + \
            context.user_email.split('@')[1]

        # Act

        response = cluedin.account.create_user(
            context, user_email, context.user_password)
        print(response)

        # Assert

        assert response.ok

    def test_create_admin_user(self):

        # Arrange

        context = Context.from_json_file(os.environ['CLUEDIN_CONTEXT'])
        context.get_token()

        user_email = f'testadmin_{random.randint(1, 1000000)}@' + \
            context.user_email.split('@')[1]

        # Act

        response = cluedin.account.create_admin_user(
            context, user_email, context.user_password)
        print(response)

        # Assert

        assert response.ok

    def test_get_user(self):

        # Arrange

        context = Context.from_json_file(os.environ['CLUEDIN_CONTEXT'])
        context.get_token()

        # Act

        response = cluedin.account.get_user(context)

        # Assert

        assert response['client']['Email'] == context.user_email

    def test_get_user_by_id(self):

        # Arrange

        context = Context.from_json_file(os.environ['CLUEDIN_CONTEXT'])
        context.get_token()
        user_id = cluedin.account.get_user(context)['client']['Id']

        # Act

        response = cluedin.account.get_user(context, user_id=user_id)

        # Assert

        assert response['client']['Id'] == user_id
        assert response['client']['Email'] == context.user_email
