#!/usr/bin/env python

# Special thank to:
# http://stackoverflow.com/questions/4994913/app-engine-default-django-version-change
from google.appengine.dist import use_library
use_library('django', '1.2')

#########################################
# Remote_API Authentication configuration.
#
# See google/appengine/ext/remote_api/handler.py for more information.
# For datastore_admin datastore copy, you should set the source appid
# value.  'HTTP_X_APPENGINE_INBOUND_APPID', ['trusted source appid here']
#
remoteapi_CUSTOM_ENVIRONMENT_AUTHENTICATION = (
    'HTTP_X_APPENGINE_INBOUND_APPID', [])
