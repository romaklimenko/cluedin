import requests

from .account import get_users
from .context import Context
from .env import CLUEDIN_REQUEST_TIMEOUT_IN_SECONDS


def post_clue(context: Context, clue: str, content_type: str = 'application/xml') -> str:
    """Post a clue to CluedIn.

    Args:
        context (Context): Context object.
        clue (str): Clue XML or JSON.
        content_type (str, optional): Content type. Defaults to 'application/xml'.
          If 'application/json', the clue is expected to be JSON.

    Returns:
        str: response text.
    """
    headers = {
        'Authorization': f'Bearer {context.access_token}',
        'Content-Type': content_type
    }
    params = {'save': 'true'}

    response = requests.post(
        url=f'{context.public_api_url}/v1/clue',
        data=clue.encode(),
        headers=headers,
        params=params,
        timeout=CLUEDIN_REQUEST_TIMEOUT_IN_SECONDS,
        verify=context.verify_tls
    )

    response.raise_for_status()

    return response.text


def restore_user_entities(context: Context) -> list:
    """Restore user entities if they are missing.
      The method gets all users for the organization and checks if they have an entity.
      If they don't, a clue is created and posted to CluedIn.

    Args:
        context (Context): Context object.

    Returns:
        list: list of results.
    """

    org_id = context.jwt_payload['OrganizationId']
    org_name = context.org_name

    results = []

    for user in get_users(context, org_id):
        if user['Entity'] is None:
            user_id = user['Account']['Id']
            user_name = user['Account']['UserName']

            # pylint: disable=line-too-long
            clue = f'''<clue organization="{org_id}" origin="/Infrastructure/User#CluedIn:{user_id}" appVersion="2.17.0.0">
          <clueDetails>
            <data inputSource="user" origin="/Infrastructure/User#CluedIn:{user_id}" appVersion="2.17.0.0">
              <processingFlags />
              <entityData id="6" origin="/Infrastructure/User#CluedIn:{user_id}" appVersion="2.17.0.0">
                <entityType>/Infrastructure/User</entityType>
                <name>{user_name}</name>
                <aliases>
                  <value>{user_id}</value>
                  <value>{user_name}</value>
                </aliases>
                <systemTagName>{user_name}</systemTagName>
                <codes>
                  <value>/Infrastructure/User#CluedIn:{user_id}</value>
                  <value>/Infrastructure/User#CluedIn:{user_name}</value>
                </codes>
                <edges>
                  <outgoing>
                    <edge type="/WorksFor" creationOptions="Default" from="C:/Infrastructure/User#CluedIn:{user_id}" to="{org_name}§C:/Organization#CluedIn:{org_id}" />
                  </outgoing>
                </edges>
                <edgesSummary />
                <properties type="/Metadata/KeyValue">
                  <property key="IsNewUser">True</property>
                  <property key="organization.name">{org_name}</property>
                  <property key="user.email">{user_name}</property>
                </properties>
              </entityData>
              <dataActions />
              <processedData ref="6" origin="/Infrastructure/User#CluedIn:{user_id}" appVersion="2.17.0.0">
                <edges />
                <edgesSummary />
                <properties type="/Metadata/KeyValue" />
                <timeToLive>0</timeToLive>
                <isShadowEntity>False</isShadowEntity>
              </processedData>
            </data>
            <references />
          </clueDetails>
        </clue>'''

            results.append({
                'user': user_name,
                'result': post_clue(context, clue)
            })
    return results
