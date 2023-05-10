import requests
from .urls import get_public_api_url
from .account import get_users


def post_clue(context, clue, content_type='application/xml'):
    headers = {
        'Authorization': 'Bearer {}'.format(context['access_token']),
        'Content-Type': content_type
    }
    params = {'save': 'true'}
    response = requests.post(
        url=f'{get_public_api_url(context)}/v1/clue',
        data=clue.encode(),
        headers=headers,
        params=params
    )

    if not response.ok:
        raise Exception({
            'status_code': response.status_code,
            'text': response.text
        })

    return response.text


def restore_user_entities(context):

    organization_id = context['jwt']['OrganizationId']
    organization = context['organization']

    results = []

    for user in get_users(context, organization_id):
        if user['Entity'] is None:
            user_id = user['Account']['Id']
            username = user['Account']['UserName']

            clue = f'''<clue organization="{organization_id}" origin="/Infrastructure/User#CluedIn:{user_id}" appVersion="2.17.0.0">
          <clueDetails>
            <data inputSource="user" origin="/Infrastructure/User#CluedIn:{user_id}" appVersion="2.17.0.0">
              <processingFlags />
              <entityData id="6" origin="/Infrastructure/User#CluedIn:{user_id}" appVersion="2.17.0.0">
                <entityType>/Infrastructure/User</entityType>
                <name>{username}</name>
                <aliases>
                  <value>{user_id}</value>
                  <value>{username}</value>
                </aliases>
                <systemTagName>{username}</systemTagName>
                <codes>
                  <value>/Infrastructure/User#CluedIn:{user_id}</value>
                  <value>/Infrastructure/User#CluedIn:{username}</value>
                </codes>
                <edges>
                  <outgoing>
                    <edge type="/WorksFor" creationOptions="Default" from="C:/Infrastructure/User#CluedIn:{user_id}" to="{organization}§C:/Organization#CluedIn:{organization_id}" />
                  </outgoing>
                </edges>
                <edgesSummary />
                <properties type="/Metadata/KeyValue">
                  <property key="IsNewUser">True</property>
                  <property key="organization.name">{organization}</property>
                  <property key="user.email">{username}</property>
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
                'user': username,
                'result': post_clue(context, clue)
            })
    return results
