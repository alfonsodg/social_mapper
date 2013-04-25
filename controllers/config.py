# -*- coding: utf-8 -*-

if False:
    import Field, T, settings, IS_IN_DB, DAL, SQLFORM
    import Session, Request, Response, auth, db, service, redirect, URL
    session = Session()
    request = Request()
    response = Response()

import xlrd

UPLOAD_PATH = 'applications/social_mapper/uploads'
EXCEL_FILE = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
OLD_EXCEL_FILE = 'application/vnd.ms-excel'
CSV_FILE = 'text/csv'

restrictions = auth.has_membership('root') or \
    auth.has_membership('configuracion')

### required - do no delete
def user():
    """
    User management
    """
    return dict(form=auth())


def download():
    """
    Download Procedures
    """
    return response.download(request, db)


def call():
    """
    Expose service
    """
    return service()
### end requires


def check_places(form):
    #place = form.vars.name
    #area = form.vars.area
    #data = db(db.places.name==place) & (db.places.area==area)).select()
    query = db.places.name == form.vars.name
    query &= db.places.area == form.vars.area
    if db(query).count():
        form.errors.user = T("Relation Between Place/Name already exists!")
    return
    #print data


@auth.requires(restrictions)
def tags():
    """
    Manage tags
    """
    form = SQLFORM(db.tag)
    if form.process().accepted:
        response.flash = T('Tag Accepted')
    form2 = SQLFORM.grid(db.tag,
                         create=False,
                         )
    return dict(form=form, form2=form2)


@auth.requires(restrictions)
def answer_types():
    """
    Manage answer types
    """
    form = SQLFORM(db.answer_types)
    if form.process().accepted:
        response.flash = T('Answer Type Accepted')
    form2 = SQLFORM.grid(db.answer_types,
                         create=False,
                         )
    return dict(form=form, form2=form2)


@auth.requires(restrictions)
def content_data():
    """
    Attachment input
    """
    #form = SQLFORM(db.contents)
    #if form.process().accepted:
        #response.flash = T('Contents Accepted')
    form = ''
    form2 = SQLFORM.grid(db.contents,
                         #create=False,
                         )
    return dict(form=form, form2=form2)


@auth.requires(restrictions)
def gis_layers():
    """
    Add GIS Layers
    """
    max_val = db.gis_layers.priority.max()
    result = db().select(max_val).first()[max_val]
    db.gis_layers.priority.default = result + 5
    form = ''
    form2 = SQLFORM.grid(db.gis_layers,
                         create=True,
                         paginate=25
                         )
    return dict(form=form, form2=form2)


@auth.requires(restrictions)
def data_types():
    """
    Add Attachment Type
    """
    form = SQLFORM(db.data_types)
    if form.process().accepted:
        response.flash = T('Data Type Accepted')
    form2 = SQLFORM.grid(db.data_types,
                         create=False,
                         )
    return dict(form=form, form2=form2)


@auth.requires(restrictions)
def periods():
    """
    Period of Time
    """
    form = SQLFORM(db.periods)
    if form.process().accepted:
        response.flash = T('Period Accepted')
    form2 = SQLFORM.grid(db.periods,
                         create=False,
                         )
    return dict(form=form, form2=form2)


@auth.requires(restrictions)
def environments():
    """
    Kind of environment
    """
    form = SQLFORM(db.environments)
    if form.process().accepted:
        response.flash = T('Environment Accepted')
    form2 = SQLFORM.grid(db.environments,
                         create=False,
                         )
    return dict(form=form, form2=form2)


@auth.requires(restrictions)
def areas():
    """
    Name of Area, the areas can be referenced for another area, building a
    tree
    """
    #form = SQLFORM(db.areas)
    #if form.process().accepted:
        #response.flash = T('Areas Accepted')
    form = ''
    form2 = SQLFORM.grid(db.areas,
                         #create=False,
                         )
    return dict(form=form, form2=form2)


@auth.requires(restrictions)
def places():
    """
    Name of a place
    """
    #form = SQLFORM(db.places)
    #if form.process(onvalidation=check_places).accepted:
    #    response.flash = T('Place Accepted')
    form = ''
    form2 = SQLFORM.grid(db.places,
                         create=False,
                         )
    return dict(form=form, form2=form2)


@auth.requires(restrictions)
def groups():
    """
    Group of work, study or analysis
    """
    #form = SQLFORM(db.groups)
    #if form.process().accepted:
        #response.flash = T('Groups Accepted')
    form = ''
    form2 = SQLFORM.grid(db.groups,
                         #create=False,
                         )
    return dict(form=form, form2=form2)


@auth.requires(restrictions)
def individuals():
    """
    People to study
    """
    #form = SQLFORM(db.individuals)
    #if form.process().accepted:
        #response.flash = T('People Accepted')
    form = ''
    form2 = SQLFORM.grid(db.individuals,
                         #create=False,
                         )
    return dict(form=form, form2=form2)


@auth.requires(restrictions)
def topics():
    """
    Topic of the Project (Title which groups activities)
    """
    #form = SQLFORM(db.topics)
    #if form.process().accepted:
        #response.flash = T('Activities Accepted')
    form = ''
    form2 = SQLFORM.grid(db.topics,
                         #create=False,
                         )
    return dict(form=form, form2=form2)


@auth.requires(restrictions)
def activities():
    """
    Activities or questions
    """
    #form = SQLFORM(db.activities)
    #if form.process().accepted:
        #response.flash = T('Activities Accepted')
    form = ''
    form2 = SQLFORM.grid(db.activities,
                         #create=False,
                         )
    return dict(form=form, form2=form2)


#@auth.requires(restrictions)
#def choices():
    #"""
    #Choices
    #"""
    #form = SQLFORM(db.choices)
    #if form.process().accepted:
        #response.flash = T('Choices Accepted')
    #form2 = SQLFORM.grid(db.choices,
                         #create=False,
                         #)
    #return dict(form=form, form2=form2)


@auth.requires(restrictions)
def projects():
    """
    Project: create or edit
    """
    form = SQLFORM(db.projects)
    if form.process().accepted:
        response.flash = T('Projects Accepted')
    form2 = SQLFORM.grid(db.projects,
                         create=False,
                         )
    return dict(form=form, form2=form2)


@auth.requires(restrictions)
def project_tree():
    """
    Relation between topic and activity
    """
    form = SQLFORM.factory(
        Field('project_name', label=T('Project Name'),
              comment=T('Ingrese el nombre del proyecto'),
              requires=IS_IN_DB(db, 'projects.id', '%(name)s')
              ),
        Field('process_file', 'upload', label=T('Spreadsheet File'),
              comment=T('Ingresar archivo pre-formateado'),
              uploadfolder=UPLOAD_PATH
              )
    )
    if form.process().accepted:
        projectname = form.vars.project_name
        filename = form.vars.process_file
        file_type = None
        if request.vars.process_file != '':
            file_type = request.vars.process_file.type
        if file_type == EXCEL_FILE or file_type == OLD_EXCEL_FILE:
            excel_process(filename, projectname)
            response.flash = 'Archivo Procesado!'
        else:
            response.flash = 'Archivo No Reconocido!'
    form2 = SQLFORM.grid(db.project_tree,
                         # create=False,
                         )
    return dict(form=form, form2=form2)


def book_tree(book):
    """
    Receive excel book and builds a complete list
    """
    topics = {}
    data_col = []
    # Get Sheets
    for sindex in range(book.nsheets):
        sheet = book.sheet_by_index(sindex)
        # Get Rows
        for pos in range(sheet.nrows):
            last_topic = False
            data_row = []
            # Get Cols
            for col in range(sheet.ncols):
                valid_data = sheet.cell_type(pos, col)
                try:
                    sample_source = int(sheet.cell_value(pos, col))
                except:
                    sample_source = sheet.cell_value(pos, col)
                if valid_data:
                    topics[col] = sample_source
                    last_topic = sample_source
                if sample_source == '' and last_topic is False:
                    try:
                        sample_source = topics[col]
                    except:
                        pass
                if sample_source:
                    data_row.append(sample_source)
            data_col.append(data_row)
    return data_col


def excel_process(filedata, projectname):
    """
    Read excel file and gets data
    """
    filename = '%s/%s' % (UPLOAD_PATH, filedata)
    book = xlrd.open_workbook(filename)
    data = book_tree(book)
    topics = {}
    reference = None
    order = 1
    norder = 1
    # Row in Data
    for line in data:
        kind = True
        last_topic = None
        pos_col = 0
        # Cols in Row
        for col in line:
            # If col type is INT then BREAK: that's' a QUESTION
            if type(col) is int:
                kind = False
                break
            if kind:
                if col not in topics:
                    if last_topic in topics:
                        value_topic = {'name': col, 'dependence':
                                       topics[last_topic], 'priority': order,
                                       'project':projectname
                                        }
                    else:
                        value_topic = {'name': col,
                                       'dependence': last_topic,
                                       'priority': order,
                                       'project':projectname
                                       }
                    reference = db.topics.update_or_insert(**value_topic)
                    if reference is None:
                        reference = db.topics((db.topics.name == col)).id
                    topics[col] = reference
                    order += 5
                last_topic = col
            pos_col += 1
        # We get last_topic as LAST TOPIC used, obvious?
        question = line[pos_col:]
        elems = len(question)
        value_question = None
        if elems == 2:
            value_question = {'priority': question[0],
                              'name': question[1]
                              }
        elif elems == 3:
            if question[2] == '-':
                question[2] = ''
            value_question = {'priority': question[0],
                              'name': question[1], 'option_data': question[2]
                              }
        elif elems == 4:
            if question[2] == '-':
                question[2] = ''
            if question[3] == '-':
                question[3] = ''
            value_question = {'priority': question[0],
                              'name': question[1], 'option_data': question[2],
                              'score_data': question[3]
                              }
        elif elems == 5:
            if question[2] == '-':
                question[2] = ''
            if question[3] == '-':
                question[3] = ''
            value_question = {'priority': question[0],
                              'name': question[1], 'option_data': question[2],
                              'score_data': question[3], 'tags': []
                              }
            for tag in question[4].split(','):
                temp = {'name': tag}
                tag_id = db.tag.update_or_insert(**temp)
                if tag_id is None:
                    tag_id = db.tag(db.tag.name == tag).id
                value_question['tags'].append(tag_id)
        if value_question:
            reference = db.activities.update_or_insert(**value_question)
            if reference is None:
                reference = db.activities(
                    (db.activities.name == question[1])).id
            value_tree = {'project': projectname,
                          'topic': topics[last_topic],
                          'activity': reference,
                          'priority': norder
                          }
            db.project_tree.update_or_insert(**value_tree)
            norder += 5
    redirect(URL('project_tree'))
