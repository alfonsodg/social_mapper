# -*- coding: utf-8 -*-
### required - do no delete
def user(): return dict(form=auth())
def download(): return response.download(request,db)
def call(): return service()
### end requires

restrictions = auth.has_membership('root')


@auth.requires(restrictions)
def users_manage():
    form = SQLFORM.grid(db.auth_user)
    return dict(form=form)


@auth.requires(restrictions)
def users_groups():
    form = SQLFORM.grid(db.auth_group)
    return dict(form=form)


@auth.requires(restrictions)
def users_membership():
    form = SQLFORM.grid(db.auth_membership)
    return dict(form=form)
