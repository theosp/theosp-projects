#!/usr/bin/env python

from google.appengine.ext import db
from google.appengine.ext.db import polymodel
from google.appengine.ext import blobstore

class FilesSystem(polymodel.PolyModel):
    # Attributes {{{
    permalink = db.StringProperty(default="new_file.txt")
    blobinfo = blobstore.BlobReferenceProperty()
    # }}}

    # Modifications date tracking {{{
    date_created = db.DateTimeProperty(auto_now_add=True)
    date_modified = db.DateTimeProperty(auto_now=True)
    # }}}

    # Created/modified by {{{
    created_by = db.UserProperty()
    modified_by = db.UserProperty()
    # }}}

# vim:fdm=marker:fmr={{{,}}}:

