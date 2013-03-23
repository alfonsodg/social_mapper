# -*- coding: utf-8 -*-

if False:
    #import Field, T, settings, IS_IN_DB, DAL, SQLFORM
    import Session, Request, Response, auth, db, service
    session = Session()
    request = Request()
    response = Response()


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


def map():
    """
    Exposes the information for the map
    """
    map_lon = request.vars.lon
    map_lat = request.vars.lat
    map_zoom = request.vars.zoom
    map_origin = request.vars.origin
    layer_data = db(db.gis_layers.status == 1).select(db.gis_layers.name,
                                                      db.gis_layers.file_data,
                                                      db.gis_layers.style_data,
                                                      db.gis_layers.rule_data,
                                                      db.gis_layers.popup,
                                                      orderby=db.gis_layers.priority|db.gis_layers.id)
    if map_lon is None:
        map_lon = -75.88400
    if map_lat is None:
        map_lat = -8.0078125
    if map_zoom is None:
        map_zoom = 8
    if map_origin is None:
        map_origin = 'sphericalm'
    return dict(layer_data=layer_data, map_lon=map_lon, map_lat=map_lat,
                map_zoom=map_zoom, map_origin=map_origin)
