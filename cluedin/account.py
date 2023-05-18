import requests

from .context import Context
from .env import CLUEDIN_REQUEST_TIMEOUT_IN_SECONDS

# Account


def get_users(context: Context, org_id: str = None) -> list:
    """Get users for an organization.

    Args:
        context (Context): Context object.
        org_id (str, optional): organization ID. Defaults to None.
            If None, the current user's organization ID is used.

    Returns:
        list: JSON response.
    """
    headers = {
        'Authorization': f'Bearer {context.access_token}'
    }

    params = {}

    if org_id is not None:
        params['organizationId'] = org_id

    response = requests.get(
        url=f'{context.auth_url}/api/account/accounts',
        headers=headers,
        params=params,
        timeout=CLUEDIN_REQUEST_TIMEOUT_IN_SECONDS,
        verify=context.verify_tls)

    if not response.ok:
        response.raise_for_status()

    return response.json()


# Availability

def is_organization_available_response(context: Context, org_name: str) -> dict:
    """Check if an organization name is available.

    Args:
        context (Context): Context object.
        org_name (str): Organization name.

    Returns:
        dict: JSON response.
    """
    headers = {
        'Authorization': f'Bearer {context.access_token}'
    }
    response = requests.get(
        url=f'{context.auth_url}/api/account/available?clientId={org_name}',
        headers=headers,
        timeout=CLUEDIN_REQUEST_TIMEOUT_IN_SECONDS,
        verify=context.verify_tls)

    if not response.ok:
        response.raise_for_status()

    return response.json()


def is_organization_available(context: Context, org_name: str) -> bool:
    """Check if an organization name is available.

    Args:
        context (Context): Context object.
        org_name (str): Organization name.

    Returns:
        bool: True if available, False otherwise.
    """
    return bool(is_organization_available_response(context, org_name)['isAvailable'])


def is_user_available_response(context: Context, user_email: str, org_name: str) -> dict:
    """Check if a user email is available.

    Args:
        context (Context): Context object.
        user_email (str): User email.
        org_name (str): Organization name.

    Returns:
        dict: JSON response.
    """
    response = requests.get(
        url=f'{context.auth_url}/api/account/username?username={user_email}&clientId={org_name}',
        timeout=CLUEDIN_REQUEST_TIMEOUT_IN_SECONDS,
        verify=context.verify_tls)

    if not response.ok:
        response.raise_for_status()

    return response.json()


def is_user_available(context: Context, user_email: str, org_name: str) -> bool:
    """Check if a user email is available.

    Args:
        context (Context): Context object.
        user_email (str): User email.
        org_name (str): Organization name.

    Returns:
        bool: True if available, False otherwise.
    """
    return bool(is_user_available_response(context, user_email, org_name)['isAvailable'])


# Registration

def get_invitation_code(context: Context, email: str) -> str:
    """Get an invitation code for a user email.

    Args:
        context (Context): (Context): Context object.
        email (str): User email.

    Returns:
        str: Invitation code.
    """
    headers = {
        'Authorization': f'Bearer {context.access_token}'
    }

    response = requests.get(
        url=f'{context.auth_url}/api/account/invitationcode?email={email}',
        headers=headers,
        timeout=CLUEDIN_REQUEST_TIMEOUT_IN_SECONDS,
        verify=context.verify_tls)

    return response.text


def create_organization(
        context: Context,
        user_email: str,
        password: str,
        org_name: str,
        org_sub_domain: str = None,
        email_domain: str = None,
        allow_email_domain_signup: bool = True,
        new_account_access_key: str = None) -> dict:
    """Create an organization with an admin user.

    Args:
        context (Context): Context object.
        user_email (str): Admin user email.
        password (str): Admin user password.
        org_name (str): Organization name.
        org_sub_domain (str, optional): Organization subdomain. Defaults to None. If None, org_name is used.
        email_domain (str, optional): Email domain. Defaults to None. If None, context.domain is used.
        allow_email_domain_signup (bool, optional): Allow email domain sign up. Defaults to True. If True, users can sign up with an email from the email domain only.
        new_account_access_key (str, optional): Used in Kubernetes to protect the endpoint. See `cluedin-new-organization-access-key` secret. Defaults to None.

    Returns:
        dict: JSON response.
    """

    headers = {}

    if new_account_access_key is not None:
        headers['x-cluedin-newaccountaccesskey'] = new_account_access_key

    if org_sub_domain is None:
        org_sub_domain = org_name

    if email_domain is None:
        email_domain = context.domain

    form_data = {
        'username': user_email,
        'email': user_email,
        'password': password,
        'confirmPassword': password,
        'organizationName': org_name,
        'applicationSubDomain': org_sub_domain,
        'emailDomain': email_domain,
        'grant_type': 'password',
        'allowEmailDomainSignup': allow_email_domain_signup
    }

    response = requests.post(
        url=f'{context.auth_url}/api/account/new',
        headers=headers,
        data=form_data,
        timeout=CLUEDIN_REQUEST_TIMEOUT_IN_SECONDS,
        verify=context.verify_tls)

    if not response.ok:
        response.raise_for_status()

    return response.json()
