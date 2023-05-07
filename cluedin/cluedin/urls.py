def get_protocol(context):
    if 'protocol' not in context:
        return 'https'
    else:
        return context['protocol']


def get_org_url(context):
    return f'{get_protocol(context)}://{context["organization"]}.{context["domain"]}'


def get_auth_url(context):
    if 'auth' in context:
        return context['auth']
    else:
        return f'{get_org_url(context)}/auth'


def get_api_url(context):
    if 'api' in context:
        return context['api']
    else:
        return f'{get_org_url(context)}/api/api'


def get_graphql_url(context):
    if 'graphql' in context:
        return context['graphql']
    else:
        return f'{get_api_url(context)}/graphql'
