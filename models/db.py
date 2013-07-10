# -*- coding: utf-8 -*-

if False:
    import Field, T, settings, Session, Request, Response, IS_IN_DB, DAL
    import SQLFORM
    session = Session()
    request = Request()
    response = Response()


import socket
hostname = socket.gethostname()

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    # db = DAL('sqlite://storage.sqlite',pool_size=1,check_reserved=['all'])
    if (hostname == 'endeavour' or hostname == 'echelon'
        or hostname == 'localhost'):
        db = DAL('postgres://alfonsodg:alfonsodg@localhost/cima',
                 pool_size=1, check_reserved=['all'])
    else:
        db = DAL('postgres://cima:cima@localhost/cima',
                 pool_size=1, check_reserved=['all'])
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore')
    ## store sessions and tickets there
    session.connect(request, response, db=db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

import datetime
from gluon.tools import Auth, Crud, Service, PluginManager#, prettydate
auth = Auth(db)
crud, service, plugins = Crud(db), Service(), PluginManager()
now = datetime.datetime.now()

## create all tables needed by auth if not custom tables
auth.define_tables(username=False, signature=False)

## configure email
mail = auth.settings.mailer
mail.settings.server = 'logging' or 'smtp.gmail.com:587'
mail.settings.sender = 'you@gmail.com'
mail.settings.login = 'username:password'

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

# auth.settings.actions_disabled.append('register')

## if you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, write your domain:api_key in private/janrain.key
from gluon.contrib.login_methods.rpx_account import use_janrain
use_janrain(auth, filename='private/janrain.key')

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

## after defining tables, uncomment below to enable auditing
auth.enable_record_versioning(db)

mail.settings.server = settings.email_server
mail.settings.sender = settings.email_sender
mail.settings.login = settings.email_login


STYLE = """
fillColor: '#AA00FF',
fillOpacity: .6,
strokeColor: '#000000',
strokeWidth: 1,
pointRadius: 8
"""


POPUP = '''"<div><strong>Nombre:</strong> <br/>" + feature.attributes.NOMBRE +
"<br/><strong>Categoria:</strong> <br/>" + feature.attributes.CATEGORIA +
"<br/><strong>Coordenadas:</strong> <br/>" + utmcoord +"</div>"'''


db.define_table('tag',
                Field('name', label=T('Name'), comment=T(
                      'Denominación del TAG')),
                format='%(name)s'
                )


db.define_table('answer_types',
                Field('name', label=T('Name'),
                      comment=T('Tipo de respuesta')),
                format='%(name)s')


db.define_table('data_types',
                Field('name', label=T('Name'),
                      comment=T('Tipo de dato')),
                format='%(name)s')


db.define_table('gis_layers',
                Field('name', label=T('Name'),
                      comment=T('Nombre de la capa')),
                Field('file_data', label=T('File Data'),
                      comment=T('Archivo de datos')),
                Field('style_data', 'text', label=T(
                      'Style Data'), comment=T('Presentación de Datos'),
                      default=STYLE),
                Field('rule_data', 'text', label=T('Rule Data'),
                      comment=T('Reglas de Datos'),
                      default=None),
                Field('popup', 'text', label=T('Popup Design'), comment=T(
                      'Diseño de Popup')),
                Field('priority', 'integer', label=T(
                      'Order'), comment=T('Posicion')),
                Field('status', label=T('Status'), comment=T(
                      'Estado'), default=1),
                format='%(name)s')


db.define_table('contents',
                Field('name', 'string', label=T('Name'), comment=T(
                      'Denominacion del adjunto')),
                Field('description', 'text', label=T('Description')),
                Field('data_type', db.data_types, label=T('Data Type'),
                      comment=T('Tipo de dato contenido')),
                Field('file_content', 'upload', label=T('Content'),
                      comment=T('Archivo origen')),
                format='%(name)s'
                )


db.define_table('periods',
                Field('name', 'string', label=T(
                      'Name'), notnull=True),
                Field('description', 'text', label=T('Description')),
                Field('start_date', 'date', label=T('Start Date'), comment=T(
                      'Fecha de inicio del periodo')),
                Field('end_date', 'date', label=T('End Date'), comment=T(
                      'Fecha de culminacion del periodo')),
                format='%(name)s'
                )


db.define_table('environments',
                Field('name', 'string', label=T('Name'), notnull=True),
                Field('description', 'text', label=T(
                      'Description')),
                Field('priority', 'integer', label=T('Priority'),
                      comment=T('Orden de visualizacion')),
                format='%(name)s'
                )


db.define_table('areas',
                Field('name', 'string', label=T(
                      'Name'), comment=T('Denominacion del area/zona'),
                      notnull=True),
                Field('description', 'text', label=T('Description')),
                Field('environment', 'integer', label=T(
                      'Environment'), comment=T('Tipo de medio ambiente')),
                Field('dependence', 'integer', label=T('Dependence'),
                      comment=T(
                          'Dependencia con otra areas (autocompletado)')),
                Field('priority', 'integer', label=T('Priority'), comment=T(
                    'Orden de visualizacion')),
                format='%(name)s'
                )


db.define_table('groups',
                Field('name', 'string', label=T('Name'), notnull=True),
                Field('description', 'text', label=T('Description')),
                Field('priority', 'integer', label=T('Priority'), comment=T(
                      'Orden de visualizacion')),
                format='%(name)s'
                )


db.define_table('individuals',
                Field('name', 'string', label=T('Name'), notnull=True),
                Field('description', 'text', label=T('Description')),
                Field('priority', 'integer', label=T('Priority'), comment=T(
                      'Orden de visualizacion')),
                format='%(name)s'
                )


db.define_table('places',
                Field('name', 'string', label=T('Name'), comment=T(
                      'Denominacion del lugar/pueblo/centro poblado'),
                      notnull=True),
                Field('description', 'text', label=T('Description')),
                Field('coordinates', 'text', label=T('Coordinates'), comment=T(
                      'Coordenadas(Puntos) del lugar de estudio')),
                Field('area', 'integer', label=T('Area'), comment=T(
                      'Area/Zona de ubicacion')),
                Field('priority', 'integer', label=T('Priority'), comment=T(
                      'Orden de visualizacion')),
                format='%(name)s'
                )


db.define_table('projects',
                Field('name', 'string', label=T(
                      'Name'), comment=T('Denominacion del proyecto'),
                      notnull=True),
                Field('description', 'text', label=T('Description')),
                format='%(name)s'
                )


db.define_table('topics',
                Field('name', 'string', label=T(
                      'Name'), comment=T('Denominacion del Topico'),
                      notnull=True),
                Field('description', 'text', label=T('Description')),
                Field('project', db.projects, label=T('Project'), comment=T(
                      'Seleccione el proyecto')),
                Field('dependence', 'integer', label=T('Dependence'),
                      comment=T('Topico de nivel superior')),
                Field('priority', 'integer', label=T('Priority'), comment=T(
                      'Orden de visualizacion')),
                format='%(name)s'
                )


db.define_table('activities',
                Field('name', 'string', label=T(
                      'Question'), comment=T('Pregunta a desarrollar'),
                      notnull=True),
                Field('description', 'text', label=T('Description')),
                Field('project', db.projects, label=T('Project'), comment=T(
                      'Seleccione el proyecto')),
                Field('kind', 'integer', label=T(
                      'Type'), comment=T('Tipo de respuesta')),
                Field('option_data', 'text', label=T('Options'), comment=T(
                      'Opciones, separadas por barra en orden deseado')),
                Field('score_data', 'string', label=T('Scores'), comment=T(
                      'Puntaje, separados por barra en orden según opción')),
                Field('tags', 'list:reference tag', label=T('Tags'), comment=T(
                      'Tags / Palabras clave')),
                Field('priority', 'integer', label=T('Priority'), comment=T(
                      'Orden de visualizacion')),
                format='%(id)s-%(name)s'
                )


db.define_table('project_tree',
                Field('project', db.projects, label=T('Project'), comment=T(
                      'Seleccione el proyecto')),
                Field('topic', db.topics, label=T('Topic'), comment=T(
                      'Seleccione el topico')),
                Field('activity', db.activities, label=T('Activity'),
                      comment=T('Seleccione la actividad')),
                Field('priority', 'integer', label=T('Priority'),
                      comment=T('Orden de visualizacion')),
                format=lambda value: project_tree_value(value, mode=1)
                )


db.define_table('main_data',
                Field(
                'register_time', 'datetime', default=now, label=T('Time')),
                Field('register_user', db.auth_user, label=T('Input User')),
                Field('name', 'string', label=T(
                      'Name'), comment=T('Denominación del Estudio'),
                      notnull=True),
                Field('description', 'text', label=T('Description')),
                Field('project', db.projects, label=T('Projects'), comment=T(
                      'Proyecto desarrollado')),
                Field('period', db.periods, label=T('Period'), comment=T(
                      'Periodo del estudio')),
                Field('place', db.places, label=T('Place'),
                      comment=T('Lugar de estudio')),
                format='%(name)s'
                )

db.define_table('detail_data',
                Field(
                'register_time', 'datetime', default=now, label=T('Time')),
                Field('register_user', db.auth_user, label=T('Input User')),
                Field('reference', db.main_data, label=T('Reference'),
                      comment=T('Denominación del estudio')),
                Field('study_group', 'integer', label=T('Group'), comment=T(
                      'Grupo objeto de estudio')),
                Field('individual', 'integer', label=T('Person'), comment=T(
                      'Sujeto de estudio')),
                Field('element_tree', db.project_tree, label=T('Activity'),
                      comment=T('Actividad seleccionada')),
                Field('choice', 'text', label=T('Answer'), comment=T(
                      'Desarrollo de la actividad (Respuesta)'), notnull=True),
                Field('comments', 'text', label=T('Comment'),
                      comment=T('Comentarios')),
                Field('value_data', 'double', label=T('Score'), comment=T(
                      'Valor Asignado')),
                Field('content_data', 'integer', label=T('Content'), comment=T(
                      'Archivo adjunto')),
                format='%(id)s'
                )


def project_tree_value(id_val, mode=0):
    """
    Project Tree Representation.
    Joins the topic and the activity.
    """
    if mode == 0:
        val_topic = db.project_tree(id_val).topic
        val_activity = db.project_tree(id_val).activity
    else:
        val_topic = id_val.topic
        val_activity = id_val.activity
    topic = db.topics(val_topic).name
    activity = db.activities(val_activity).name
    return '%s - %s' % (topic, activity)


def content_data_value(id_val):
    """
    Content Data Representation
    """
    try:
        val_content_data = db.contents(value).name
    except:
        val_content_data = ''
    return '%s' % val_content_data


def topic_value(id_val):
    """
    Content Data Representation
    """
    try:
        val_topic = db.topics(id_val).name
    except:
        val_topic = T('ERROR: Inconsistency')
    return '%s' % val_topic

def name_data(table, id_val):
    """
    Content Data Representation
    """
    try:
        value_data = table(id_val).name
    except:
        value_data = ''
    return '%s' % value_data


db.tag.name.requires = IS_NOT_IN_DB(db, 'tag.name')
db.projects.name.requires = IS_NOT_IN_DB(db, 'projects.name')
#db.places.name.requires = IS_NOT_IN_DB(db, 'places.name')
db.periods.name.requires = IS_NOT_IN_DB(db, 'periods.name')
#db.individuals.name.requires = IS_NOT_IN_DB(db, 'individuals.name')
db.groups.name.requires = IS_NOT_IN_DB(db, 'groups.name')
#db.areas.name.requires = IS_NOT_IN_DB(db, 'areas.name')
db.environments.name.requires = IS_NOT_IN_DB(db, 'environments.name')
db.contents.name.requires = IS_NOT_IN_DB(db, 'contents.name')
db.gis_layers.name.requires = IS_NOT_IN_DB(db, 'gis_layers.name')
db.answer_types.name.requires = IS_NOT_IN_DB(db, 'answer_types.name')
db.data_types.name.requires = IS_NOT_IN_DB(db, 'data_types.name')
# db.choices.kind.requires = IS_IN_SET(answer_type)
# db.contents.data_type.requires = IS_IN_SET(data_type)
# db.choices.kind.requires = IS_IN_DB(db, 'answer_types.id')
db.contents.data_type.requires = IS_IN_DB(db, 'data_types.id', '%(name)s')
# db.areas.requires = IS_IN_DB(db, 'areas.id')
# db.topics.requires = IS_IN_DB(db, 'topics.id')
# db.detail_data.requires = IS_IN_DB(db, 'contents.id')
# db.zones.dependence.requires = IS_IN_DB(db,'zones.id','%(name)s')
# db.detail_data.study_group.requires = IS_IN_DB(db,'groups.id','%(name)s')
# db.detail_data.individual.requires = IS_IN_DB(db,'individuals.id','%(name)s')
db.topics.dependence.represent = lambda value, row: None if value is None else name_data(db.topics, value)
db.places.area.represent = lambda value, row: None if value is None else name_data(db.areas, value)
#db.topics.dependence.represent = lambda value, row: db.topics[value].name or None
#db.project_tree.id.represent = lambda value, row: None if value is None else project_tree_value(value)
db.contents.data_type.represent = lambda value, row: None if value is None else name_data(db.data_types, value)
db.detail_data.study_group.represent = lambda value, row: None if value is None else name_data(db.groups, value)
db.detail_data.individual.represent = lambda value, row: None if value is None else name_data(db.individuals, value)
#db.detail_data.content_data.represent = lambda value, row: None if value is None else db.contents(value).name
db.detail_data.content_data.represent = lambda value, row: None if value is None else name_data(db.contents, value)
db.areas.environment.represent = lambda value, row: None if value is None else name_data(db.environments, value)
db.areas.dependence.represent = lambda value, row: None if value is None else name_data(db.areas, value)
db.areas.environment.widget = SQLFORM.widgets.autocomplete(
    request, db.environments.name, limitby=(0, 10),
    id_field= db.environments.id, min_length=2)
db.areas.dependence.widget = SQLFORM.widgets.autocomplete(
    request, db.areas.name, limitby=(0, 10),
    id_field= db.areas.id, min_length=2)
db.places.area.widget = SQLFORM.widgets.autocomplete(
    request, db.areas.name, limitby=(0, 10),
    id_field= db.areas.id, min_length=2)
db.topics.project.widget = SQLFORM.widgets.autocomplete(
    request, db.projects.name, limitby=(0, 10),
    id_field= db.projects.id, min_length=2)
db.topics.dependence.widget = SQLFORM.widgets.autocomplete(
    request, db.topics.name, limitby=(0, 10),
    id_field= db.topics.id, min_length=2)
db.project_tree.topic.widget = SQLFORM.widgets.autocomplete(
    request, db.topics.name, limitby=(0, 10),
    id_field= db.topics.id, min_length=2)
db.project_tree.activity.widget = SQLFORM.widgets.autocomplete(
    request, db.activities.name, limitby=(0, 10),
    id_field= db.activities.id, min_length=2)
db.detail_data.reference.widget = SQLFORM.widgets.autocomplete(
    request, db.main_data.name, limitby=(0, 10),
    id_field= db.main_data.id, min_length=2)
db.detail_data.study_group.widget = SQLFORM.widgets.autocomplete(
    request, db.groups.name, limitby=(0, 10),
    id_field= db.groups.id, min_length=2)
db.detail_data.individual.widget = SQLFORM.widgets.autocomplete(
    request, db.individuals.name, limitby=(0, 10),
    id_field= db.individuals.id, min_length=2)
db.detail_data.content_data.widget = SQLFORM.widgets.autocomplete(
    request, db.contents.name, limitby=(0, 10),
    id_field= db.contents.id, min_length=2)
db.activities.kind.widget = SQLFORM.widgets.autocomplete(
    request, db.answer_types.name, limitby=(0, 10),
    id_field= db.answer_types.id, min_length=2)
