response.title = settings.title
response.subtitle = settings.subtitle
response.meta.author = '%(author)s <%(author_email)s>' % settings
response.meta.keywords = settings.keywords
response.meta.description = settings.description
inicio = [
    (T('Index'), False, URL('default','index'),[
    ]),
    ]
admin = [
    (T('Administration'), False, False,
    [
        (T('Users Manage'), False, URL('manage', 'users_manage'),[]),
        (T('Users Groups'), False, URL('manage', 'users_groups'),[]),
        (T('Users Membership'), False, URL('manage', 'users_membership'),[]),
    ]),
    ]
config = [
    (T('Configuration'), False, False,
    [
        (T('---Básicos---'), False, False),
        (T('Projects'), False, URL('config', 'projects')),
        (T('Periods'), False, URL('config', 'periods')),
        (T('Places'), False, URL('config', 'places')),
        (T('Project Tree'), False, URL('config', 'project_tree')),
        (T('---Nivel 1---'), False, False),
        (T('Topics'), False, URL('config', 'topics')),
        (T('Activities'), False, URL('config', 'activities')),
        (T('Groups'), False, URL('config', 'groups')),
        (T('---Nivel 2---'), False, False),
        (T('Individuals'), False, URL('config', 'individuals')),
        (T('Tags'), False, URL('config', 'tags')),
        (T('Answer Types'), False, URL('config', 'answer_types')),
        (T('Data Types'), False, URL('config', 'data_types')),
        (T('Content Data'), False, URL('config', 'content_data')),
        (T('---Nivel 3---'), False, False),
        (T('Environments'), False, URL('config', 'environments')),
        (T('Areas'), False, URL('config', 'areas')),
        (T('---GIS---'), False, False),
        (T('Define Layers'), False, URL('config', 'gis_layers')),
    ]),
    ]
inputdata = [
    (T('Projects'), False, False,[
        (T('Place Definition'), False, URL('data', 'main_data')),
        (T('Detailed Information'), False, URL('data', 'detail_data')),
        ('----------', False, False),
        #(T('Content Data'), False, URL('data', 'content_data')),
        #(T('Designed structure'), False, URL('data', 'format_data')),
        (T('Masive input'), False, URL('data', 'design_data')),
    ]),
    ]
information =  [
    (T('Reports'), False, False,[
        (T('Projects'), False, URL('data', 'format_data')),
    ]),
    (T('GIS'), False, False,[
        (T('Search Place'), False, URL('gis', 'search_map')),
        (T('Maps'), False, A(T('Maps'), _href=URL('gis','map'), _target="_blank")),
    ]),
]

if not auth.user:
    response.menu = inicio
elif auth.has_membership(user_id=auth.user.id, role='root'):
    response.menu = inicio
    response.menu += admin
    response.menu += config
    response.menu += inputdata
    response.menu += information
elif auth.has_membership(user_id=auth.user.id, role='configuracion'):
    response.menu = inicio
    response.menu += config
    response.menu += inputdata
    response.menu += information
elif auth.has_membership(user_id=auth.user.id, role='estandar'):
    response.menu = inicio
    response.menu += inputdata
    response.menu += information
else:
    response.menu = inicio
    response.menu += information

#if not auth.user:
    #response.menu = []
#else:
    #response.menu = options
#if not auth.user:
    #response.menu = []
#else:
    #response.menu = options
