#!/usr/bin/env python

from google.appengine.ext import db
from apis.models.files_system import FilesSystem

class {{ camelcased_entity_name }}(FilesSystem):
    pass

# vim:fdm=marker:fmr={{{,}}}:
