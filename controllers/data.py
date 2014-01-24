# -*- coding: utf-8 -*-


import xlrd
#import plugin_appreport
#import os
#from gluon.contrib.fpdf import FPDF, HTMLMixin
#import requests
#from os.path import basename
#from gluon.contrib.pyfpdf import FPDF, HTMLMixin


UPLOAD_PATH = 'applications/social_mapper/uploads'
EXCEL_FILE = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
OLD_EXCEL_FILE = 'application/vnd.ms-excel'
CSV_FILE = 'text/csv'

restrictions = auth.has_membership('root') or \
    auth.has_membership('configuracion') or \
    auth.has_membership('estandar')


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


@auth.requires(restrictions)
def show():
    contents = db.contents(request.args(0,cast=int)) or redirect(URL('index'))
    name_data = contents.file_content
    contentfile = '%s/%s' % (UPLOAD_PATH, name_data)
    return response.stream(open(contentfile,'rb'), chunk_size=10**6)


@auth.requires(restrictions)
def main_data():
    """
    Manage Project Main data
    """
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
    """
    Additional information to the Main data
    """
    db.detail_data.register_user.default = auth.user.id
    db.detail_data.register_user.writable = False
    db.detail_data.register_time.writable = False
    form = ''
    #form = SQLFORM(db.detail_data)
    #if form.process().accepted:
    #    response.flash = T('Row Accepted')
    form2 = SQLFORM.grid(db.detail_data,
                         create=True,
                         )
    return dict(form=form, form2=form2)


def format_data():
    """
    General Report view / form
    """
    data_places = db(db.main_data.project==request.vars.project_id).select(
        db.places.id, db.places.name,
        left=db.places.on(
        db.places.id == db.main_data.place),
        )
    data_topics = db(db.topics.project==request.vars.project_id).select(
        db.topics.id, db.topics.name,
        )
    #print data_places
    places = [(str(elem.id), elem.name) for elem in data_places]
    topics = [(str(elem.id), elem.name) for elem in data_topics]
    topics.append((0,'TODOS'))
    #db.patients.patient.requires = IS_IN_SET(patients)
    form = SQLFORM.factory(
        Field('project_id', db.projects, label=T('Project Name'),
              comment=T('Ingrese el nombre del proyecto'),
              
              #widget=SQLFORM.widgets.autocomplete(request,
                                                  #db.projects.name, limitby=(
                                                      #0, 10),
                                                  #id_field=db.projects.id,
                                                  #min_length=2),
              requires=IS_IN_DB(db, 'projects.id', '%(name)s', zero=T('Elegir Proyecto'))
              ),
        Field('place_id', db.places, label=T('Place Name'),
              comment=T('Ingrese el nombre del lugar'),
              #widget=SQLFORM.widgets.autocomplete(request,
                                                  #db.places.name, limitby=(
                                                      #0, 10),
                                                  #id_field=db.places.id,
                                                  #min_length=2),
              requires=IS_IN_SET(places, zero=T('Elegir Poblado'), error_message=T('Hay un problema en su selección'))
              #requires=IS_IN_DB(db, 'places.id', '%(name)s')
              ),
        Field('topic_id', label=T('Topic Name'),
              comment=T('Ingrese el nombre del topico'),
              requires=IS_IN_SET(topics, zero=T('Elegir Tópico'), error_message=T('Hay un problema en su selección')),
              # widget=SQLFORM.widgets.autocomplete(request,
              #                                     db.topics.name, limitby=(
              #                                         0, 10),
              #                                     id_field=db.topics.id,
              #                                     min_length=2),
              # requires=IS_IN_DB(db, 'topics.id', '%(name)s')
              ),
        Field('pdf', 'boolean', label=T('PDF'), comment=T('Exportar a PDF?'))
    )
    form.attributes['_id'] = 'format_data'
    tree_base = []
    tree_data = {}
    data_val = {}
    project_name = False
    project_description = False
    place_name = False
    place_coords = False
    topic_mode = False
    topic_id = False
    pdf = False
    if form.process().accepted:
        # Get Results from topics
        project_id = form.vars.project_id
        place_id = form.vars.place_id
        topic_id = form.vars.topic_id
        pdf = form.vars.pdf
        if project_id is not '':
            project_name = db.projects[project_id].name
            project_description = db.projects[project_id].description
        if place_id is not '':
            place_name = db.places[place_id].name
            place_coords = db.places[place_id].coordinates
        if topic_id is not '':
            topic_id = int(topic_id)
            if topic_id != 0:
                topic_mode = True
        #results = db(db.project_tree.project==project_id).select(
            #db.topics.ALL,
            #left=db.topics.on(
                #db.project_tree.topic == db.topics.id),
            #orderby=db.topics.priority|db.topics.id)
        results = db(db.topics.project==project_id).select(
            db.topics.id, db.topics.name,
            orderby=db.topics.priority|db.topics.id
        )
        #print results
        for row in results:
            tree_base.append({row.id: row.name})
        # Get Results from project_tree
        results = db(db.project_tree.project==project_id).select(
                              db.project_tree.topic, db.activities.name,
                              db.project_tree.project, db.project_tree.id,
                              db.activities.option_data,
                              left=db.activities.on(
                              db.project_tree.activity == db.activities.id),
                              orderby=db.project_tree.priority)
        #print results
        for row in results:
            tree_data.setdefault(row.project_tree.topic, list()).append(
                [row.project_tree.id, row.activities.name,
                 row.activities.option_data])
        if project_id is not '' and place_id is not '':
            #print project_id, place_id
            results = db((db.main_data.project == project_id)
                         & (db.main_data.place == place_id)).select(
                             db.groups.name, db.individuals.name,
                             db.detail_data.element_tree,
                             db.detail_data.choice, db.groups.description,
                             db.detail_data.content_data,
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
            for row in results:
                # print row
                data_val.setdefault(
                    row.detail_data.element_tree, list()).append(
                        [row.groups.name, row.groups.description,
                            row.individuals.name, row.detail_data.choice,
                            row.detail_data.content_data])
    if pdf:
        pass
        #redirect(URL('listing', vars=dict(html=html)))

        #return plugin_appreport.REPORTPYFPDF(html=static_html)
        #redirect(URL('report_pisa', vars=dict(html=html)))
    #     redirect(URL('report_pdf',
    #                  vars=dict(project_name=project_name,
    #                            place_name=place_name,
    #                            tree_base=tree_base,
    #                            tree_data=tree_data,
    #                            data_val=data_val,
    #                            topic_id=topic_id,
    #                            topic_mode=topic_mode
    #)))
        # report_pdf(tree_base, tree_data, project_name,
        #            project_description, data_val, place_name,
        #            topic_id, topic_mode)
    else:
        return dict(form=form, tree_base=tree_base, tree_data=tree_data,
                    project_name=project_name,
                    project_description=project_description,
                    data_val=data_val,
                    place_name=place_name, topic_id=topic_id,
                    topic_mode=topic_mode, place_coords=place_coords)




@auth.requires(restrictions)
def design_data():
    """
    Massive input of project through one form and excel file
    """
    db.detail_data.register_user.default = auth.user.id
    # db.detail_data.register_user.writable = False
    # db.detail_data.register_time.writable = False
    form = SQLFORM.factory(db.main_data,
                           Field('process_file',
                                 'upload', uploadfolder=UPLOAD_PATH),
                           )
    #print form
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
                #print valid_data
                #print sheet.cell_value(pos, col)
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
                else:
                    if valid_data == 2 and sample_source == 0:
                        data_row.append(sample_source)
            data_col.append(data_row)
    return data_col


def excel_process(filedata, data):
    """
    Read excel file, gets the books
    """
    filename = '%s/%s' % (UPLOAD_PATH, filedata)
    book = xlrd.open_workbook(filename)
    data_excel = book_tree(book)
    elems = len(data_excel)
    if elems <= 0:
        return T('Archivo sin registros procesables o con problemas.')
    #data['project'] = form.vars.project
    #data['name'] = form.vars.name
    #data['description'] = form.vars.description
    #data['period'] = form.vars.period
    #data['place'] = form.vars.place
    #main_id = db.main_data.update_or_insert(**data)
    #db((db.main_data.name == data['name']) &
            #(db.main_data.project == data['project']) &
            #(db.main_data.period == data['period']) &
            #(db.main_data.place == data['place'])
            #).delete()
    main_id = db.main_data.update_or_insert(**data)
    if main_id is None:
        main_id = db.main_data(
            (db.main_data.name == data['name']) &
            (db.main_data.project == data['project'])).id
    count = 0
    check_id = 1
    #print "main:", main_id
    #print data_excel
    #try:
    for line in data_excel:
        if len(line) < 4:
            continue
        if line[0].find(':') >= 1:
            study_group, individual = line[0].split(':')
        else:
            study_group = line[0]
            individual = None
        topic_id = db.topics((db.topics.name == line[1]) & (db.topics.project == data['project'])).id
        #print "--------"
        #print "Valores:",topic_id
        #print "pregunta:", line[3]
        activities_data = db((db.activities.name == line[3]) & (db.activities.project == data['project'])).select(db.activities.id)
        activities_count = len(activities_data.as_list())
        #print "data:",activities_data, "cuenta:",activities_count
        #print activities_count,"ALLL"
        if activities_count == 1:
            activity_id = activities_data[0].id
            check_id = activity_id
        elif activities_count > 1:
            activity_id = check_id + 1
            check_id = activity_id
            #elems = [part['id'] for part in activities_data.as_list()]
        else:
            return_message = T('Error. Revise las actividades!')
        #activity_id = db.activities(db.activities.name == line[3]).id
        #print line[3], topic_id, activity_id
        element_id = db.project_tree((db.project_tree.topic == topic_id) &
            (db.project_tree.activity == activity_id)).id
        group_id = None
        individual_id = None
        try:
            answer = line[4]
        except:
            answer = ''
        try:
            value_data = line[5]
        except:
            value_data = None
        #try:
            #content_data = requests.get(line[5])
            #name_data = basename(line[5])
            ##name_data = name_data.split('.')[0]
        #except:
            #content_data = False
            #content_id = None
        #if content_data:
            #contentfile = '%s/%s' % (UPLOAD_PATH, name_data)
            #open(contentfile, 'w').write(content_data.content)
            #stream = open(contentfile, 'rb')
            #content_id = db.contents(db.contents.name==name_data)
            #if content_id is None:
                ##content_id = db.contents.update_or_insert(
                ##    file_content=stream, name=name_data)
                #content_id = db.contents.update_or_insert(
                #file_content=db.contents.file_content.store(
                #stream, contentfile),
                #name=name_data)
            ##if content_id is None:
                ##content_id = db.contents(db.contents.name==name_data).id
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
                            'individual': individual_id,
                            #'content_data': content_id,
                            'value_data': value_data
                            }
            status = db.detail_data.update_or_insert(**value_detail)
            if status is not None:
                count += 1
    return_message = T(
        'Archivo analizado. Número de registros procesados: %s' % count)
    #except Exception, error:
    #    print error
    #    return_message = T(
    #        'Error en el procesamiento del archivo. Revise los datos!')
    return return_message


def demo():
    topics = db(db.topics.priority > 0).select(db.topics.priority)
    last_value = topics.last().priority
    print last_value,'<----Valor'
    data = db.activities(db.activities.name == "¿Por qué?").id
    mon = db(db.activities.name == "¿Por qué?").select(db.activities.id)
    elems = [l['id'] for l in mon.as_list()]

    print data
    print mon.as_list()
    print mon
    print len(mon)
    print mon[0].id

