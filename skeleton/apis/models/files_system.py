#!/usr/bin/env python

from apis.models import {{ project_underscored_name }}_data_models
from google.appengine.ext import db
from google.appengine.ext.db import polymodel
from google.appengine.ext import blobstore

class FilesSystem({{ project_underscored_name }}_data_models.{{ project_camel_cased_name }}PolyModel):
    # Attributes {{{
    permalink = db.StringProperty(default="new_file.txt")
    blobinfo = blobstore.BlobReferenceProperty()
    # }}}

# vim:fdm=marker:fmr={{{,}}}:

