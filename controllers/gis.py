# -*- coding: utf-8 -*-
### required - do no delete
def user(): return dict(form=auth())
def download(): return response.download(request,db)
def call(): return service()
### end requires
def index():
    return dict()

def error():
    return dict()
    
def map():
    layer_data = db(db.gis_layers.status==1).select(db.gis_layers.name,
        db.gis_layers.file_data, db.gis_layers.style_data,
        db.gis_layers.rule_data, db.gis_layers.popup, orderby=db.gis_layers.priority|db.gis_layers.id)
    return dict(layer_data=layer_data)
