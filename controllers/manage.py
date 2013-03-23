# -*- coding: utf-8 -*-

if False:
    import SQLFORM
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

restrictions = auth.has_membership('root')


@auth.requires(restrictions)
def users_manage():
    """
    Manage Users
    """
    form = SQLFORM.grid(db.auth_user)
    return dict(form=form)


@auth.requires(restrictions)
def users_groups():
    """
    Manage Groups
    """
    form = SQLFORM.grid(db.auth_group)
    return dict(form=form)


@auth.requires(restrictions)
def users_membership():
    """
    Manage relation between users and groups
    """
    form = SQLFORM.grid(db.auth_membership)
    return dict(form=form)
