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
    return dict()
    
def map_alt():
    layer_data = db(db.gis_layers.status==1).select(db.gis_layers.name,
        db.gis_layers.file_data, db.gis_layers.color_fill,
        db.gis_layers.color_line)
    return dict(layer_data=layer_data)
