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
    map_lon=request.vars.lon
    map_lat=request.vars.lat
    map_zoom=request.vars.zoom
    map_origin=request.vars.origin
    layer_data = db(db.gis_layers.status==1).select(db.gis_layers.name,
        db.gis_layers.file_data, db.gis_layers.style_data,
        db.gis_layers.rule_data, db.gis_layers.popup, orderby=db.gis_layers.priority|db.gis_layers.id)
    if map_lon is None:
        map_lon = -75.88400
    if map_lat is None:
        map_lat = -8.0078125
    if map_zoom is None:
        map_zoom = 8
    if map_origin is None:
        map_origin = 'sphericalm'
    return dict(layer_data=layer_data, map_lon=map_lon, map_lat=map_lat, map_zoom=map_zoom, map_origin=map_origin)
