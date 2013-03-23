# -*- coding: utf-8 -*-

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


def index():
    return dict()


def error():
    return dict()


@auth.requires_login()
def configuration():
    return dict()


@auth.requires_login()
def data():
    return dict()
