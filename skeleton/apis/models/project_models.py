#!/usr/bin/env python

from google.appengine.ext import db
from google.appengine.ext.db.polymodel import PolyModel

class {{ project_camel_cased_name }}Model(db.Model):
    # modifications date tracking {{{
    date_created = db.DateTimeProperty(auto_now_add=True)
    date_modified = db.DateTimeProperty(auto_now=True)
    # }}}

    # created/modified by {{{
    created_by = db.UserProperty()
    modified_by = db.UserProperty()
    # }}}


class {{ project_camel_cased_name }}Expando(db.Expando):
    # modifications date tracking {{{
    date_created = db.DateTimeProperty(auto_now_add=True)
    date_modified = db.DateTimeProperty(auto_now=True)
    # }}}

    # created/modified by {{{
    created_by = db.UserProperty()
    modified_by = db.UserProperty()
    # }}}


class {{ project_camel_cased_name }}PolyModel(PolyModel):
    # modifications date tracking {{{
    date_created = db.DateTimeProperty(auto_now_add=True)
    date_modified = db.DateTimeProperty(auto_now=True)
    # }}}

    # created/modified by {{{
    created_by = db.UserProperty()
    modified_by = db.UserProperty()
    # }}}


# vim:fdm=marker:fmr={{{,}}}:
