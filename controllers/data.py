# -*- coding: utf-8 -*-

import xlrd

UPLOAD_PATH = 'applications/social_mapper/uploads'
EXCEL_FILE = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
OLD_EXCEL_FILE = 'application/vnd.ms-excel'
CSV_FILE = 'text/csv'

restrictions = auth.has_membership('root') or \
    auth.has_membership('configuracion') or \
    auth.has_membership('estandar')


### required - do no delete
def user():
    return dict(form=auth())


def download():
    return response.download(request, db)


def call():
    return service()
### end requires


@auth.requires(restrictions)
def main_data():
    db.main_data.register_user.default = auth.user.id
    db.main_data.register_user.writable = False
    db.main_data.register_time.writable = False
    form = SQLFORM(db.main_data)
    if form.process().accepted:
        response.flash = T('Header Accepted')
    form2 = SQLFORM.grid(db.main_data,
                         create=False,
                         )
    return dict(form=form, form2=form2)


@auth.requires(restrictions)
def detail_data():
    db.detail_data.register_user.default = auth.user.id
    db.detail_data.register_user.writable = False
    db.detail_data.register_time.writable = False
    form = SQLFORM(db.detail_data)
    if form.process().accepted:
        response.flash = T('Row Accepted')
    form2 = SQLFORM.grid(db.detail_data,
                         create=False,
                         )
    return dict(form=form, form2=form2)


@auth.requires(restrictions)
def content_data():
    form = SQLFORM(db.contents)
    if form.process().accepted:
        response.flash = T('Contents Accepted')
    form2 = SQLFORM.grid(db.contents,
                         create=False,
                         )
    return dict(form=form, form2=form2)


def format_data():
    # data_places = db(db.places.id==request.vars.project_id).select(
    # db.places.id, db.places.name)
    # places = [(str(elem.id), elem.name) for elem in data_places]
    # db.patients.patient.requires = IS_IN_SET(patients)
    form = SQLFORM.factory(
        Field('project_id', label=T('Project Name'),
              comment=T('Ingrese el nombre del proyecto'),
              widget=SQLFORM.widgets.autocomplete(request,
                                                  db.projects.name, limitby=(
                                                      0, 10),
                                                  id_field=db.projects.id,
                                                  min_length=2),
              requires=IS_IN_DB(db, 'projects.id', '%(name)s')
              ),
        Field('place_id', label=T('Place Name'),
              comment=T('Ingrese el nombre del lugar'),
              widget=SQLFORM.widgets.autocomplete(request,
                                                  db.places.name, limitby=(
                                                      0, 10),
                                                  id_field=db.places.id,
                                                  min_length=2),
              # requires=IS_IN_DB(db, 'places.id', '%(name)s')
              ),
        Field('topic_id', label=T('Topic Name'),
              comment=T('Ingrese el nombre del topico'),
              widget=SQLFORM.widgets.autocomplete(request,
                                                  db.topics.name, limitby=(
                                                      0, 10),
                                                  id_field=db.topics.id,
                                                  min_length=2),
              # requires=IS_IN_DB(db, 'topics.id', '%(name)s')
              ),
    )
    tree_base = []
    tree_data = {}
    data_val = {}
    project_name = False
    place_name = False
    place_coords = False
    topic_mode = False
    topic_id = False
    if form.process().accepted:
        # Get Results from topics
        project_id = form.vars.project_id
        place_id = form.vars.place_id
        topic_id = form.vars.topic_id
        if project_id is not '':
            project_name = db.projects[project_id].name
        if place_id is not '':
            place_name = db.places[place_id].name
            place_coords = db.places[place_id].coordinates
        if topic_id is not '':
            topic_mode = True
            topic_id = int(topic_id)
        results = db(
        ).select(db.topics.ALL, orderby=db.topics.priority|db.topics.id)
        for row in results:
            tree_base.append({row.id: row.name})
        # Get Results from project_tree
        results = db().select(db.project_tree.topic, db.activities.name,
                              db.project_tree.project, db.project_tree.id,
                              db.activities.option_data,
                              left=db.activities.on(
                              db.project_tree.activity == db.activities.id),
                              orderby=db.project_tree.priority)
        for row in results:
            tree_data.setdefault(row.project_tree.topic, list()).append(
                [row.project_tree.id, row.activities.name,
                 row.activities.option_data])
        if project_id is not '' and place_id is not '':
            results = db((db.main_data.project == project_id)
                         & (db.main_data.place == place_id)).select(
                             db.groups.name, db.individuals.name,
                             db.detail_data.element_tree,
                             db.detail_data.choice,
                             left=(
                                 db.detail_data.on(
                                     db.main_data.id ==
                                     db.detail_data.reference),
                                 db.groups.on(
                                     db.groups.id ==
                                     db.detail_data.study_group),
                                 db.individuals.on(
                                     db.individuals.id ==
                                     db.detail_data.individual)
                             ),
                             orderby = db.detail_data.id
                         )
            # print results
            for row in results:
                # print row
                data_val.setdefault(
                    row.detail_data.element_tree, list()).append(
                        [row.groups.name, row.individuals.name,
                         row.detail_data.choice])
    return dict(form=form, tree_base=tree_base, tree_data=tree_data,
                project_name=project_name, data_val=data_val,
                place_name=place_name, topic_id=topic_id,
                topic_mode=topic_mode, place_coords=place_coords)


@auth.requires(restrictions)
def design_data():
    db.detail_data.register_user.default = auth.user.id
    # db.detail_data.register_user.writable = False
    # db.detail_data.register_time.writable = False
    form = SQLFORM.factory(db.main_data,
                           Field('process_file',
                                 'upload', uploadfolder=UPLOAD_PATH),
                           )
    print form
    form.vars.register_user = auth.user.id
    if form.process().accepted:
        data = {}
        data['project'] = form.vars.project
        data['name'] = form.vars.name
        data['description'] = form.vars.description
        data['period'] = form.vars.period
        data['place'] = form.vars.place
        filename = form.vars.process_file
        file_type = request.vars.process_file.type
        if file_type == EXCEL_FILE or file_type == OLD_EXCEL_FILE:
            # print 'SI'
            # print project_value, name_value, description_value
            status = excel_process(filename, data)
            response.flash = status
            # redirect(URL('design_data'))
        else:
            response.flash = 'Archivo No Reconocido!'
    return dict(form=form)


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


def excel_process(filedata, data):
    filename = '%s/%s' % (UPLOAD_PATH, filedata)
    book = xlrd.open_workbook(filename)
    data_excel = book_tree(book)
    elems = len(data_excel)
    if elems <= 0:
        return T('Archivo sin registros procesables o con problemas.')
    main_id = db.main_data.update_or_insert(**data)
    count = 0
    try:
        for line in data_excel:
            if len(line) < 4:
                continue
            if line[0].find(':') >= 1:
                    study_group, individual = line[0].split(':')
            else:
                    study_group = None
                    individual = None
            topic_id = db.topics(db.topics.name == line[1]).id
            activity_id = db.activities(db.activities.name == line[3]).id
            element_id = db.topics((db.project_tree.topic == topic_id) & (
                db.project_tree.activity == activity_id)).id
            group_id = None
            individual_id = None
            try:
                answer = line[4]
            except:
                answer = ''
            if study_group is not None:
                group_id = db.groups.update_or_insert(**{'name': study_group})
                if group_id is None:
                    group_id = db.groups(db.groups.name == study_group).id
            if individual is not None:
                individual_id = db.individuals.update_or_insert(
                    **{'name': individual})
                if individual_id is None:
                    individual_id = db.individuals(
                        db.individuals.name == individual).id
            if main_id is not None:
                value_detail = {'reference': main_id,
                                'element_tree': element_id, 'choice': answer,
                                'study_group': group_id,
                                'individual': individual_id
                                }
                status = db.detail_data.update_or_insert(**value_detail)
                if status is not None:
                    count += 1
        return_message = T(
            'Archivo analizado. Número de registros procesados: %s' % count)
    except:
        return_message = T(
            'Error en el procesamiento del archivo. Revise los datos!')
    return return_message
