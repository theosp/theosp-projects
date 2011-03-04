#!/usr/bin/env python

###########################################################
# Solve bug: http://groups.google.com/group/google-appengine-python/browse_thread/thread/e3a9d8b8be36870d/5dc96ab56b889dc6?pli=1
# Remove the standard version of Django and put version 1.1
import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from appengine_django import InstallAppengineHelperForDjango
InstallAppengineHelperForDjango(version='1.1')
###########################################################

# imports {{{
from google.appengine.ext import webapp, db
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

from lib import simplejson as json
from django.utils.datastructures import SortedDict

from google.appengine.api import users

from urlparse import urlparse

import os

from apis.models.{{ underscored_entity_name }} import {{ camelcased_entity_name }}
from apis.helpers.paging import PagedQuery

from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
# }}}

# helpers {{{
from datetime import datetime, date
class JsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return '**new Date(%i,%i,%i,%i,%i,%i)' % (obj.year,
                                                      obj.month-1,
                                                      obj.day,
                                                      obj.hour,
                                                      obj.minute,
                                                      obj.second)

        if isinstance(obj, date):
            return '**new Date(%i,%i,%i)' % (obj.year,
                                             obj.month-1,
                                             obj.day)

        if isinstance(obj, db.Model):
            dict_representation = {}
            for field in obj.fields():
                dict_representation[field] = getattr(obj, field)

            return dict_representation

        return obj.__dict__

def _get_path_{{ underscored_entity_name }}(path):
    "Get the {{ readable_noncapitalized_entity_name }} object of the url path's {{ readable_noncapitalized_entity_name }} key"

    {{ underscored_entity_name }}_key = urlparse(path).path.split('/')[2]

    try:
        {{ underscored_entity_name }} = db.get(db.Key({{ underscored_entity_name }}_key))
    except db.BadKeyError:
        return (400, {'error': 'InvalidKey'})

    return (200, {{ underscored_entity_name }})
# }}}

# All {{{
class All(webapp.RequestHandler):
    """Return an object with all the {{ readable_noncapitalized_pluralized_entity_name }} objects
    """
    def get(self):
        page_size = self.request.GET.get('page_size') or 30
        page = self.request.GET.get('page') or 1
        order_by = self.request.GET.get('order_by') or '-date_modified'

        page = int(page)

        {{ underscored_pluralized_entity_name }}_query = {{ camelcased_entity_name }}.all().order(order_by)
        paged_query = PagedQuery({{ underscored_pluralized_entity_name }}_query, page_size)

        results = paged_query.fetch_page(page)
        pages_count = paged_query.page_count()

        response = {'{{ underscored_pluralized_entity_name }}': SortedDict(), 'pager': {'pages_count': pages_count}}
        for {{ underscored_entity_name }} in results:
            key = str({{ underscored_entity_name }}.key())
            response['{{ underscored_pluralized_entity_name }}'][key] = {{ underscored_entity_name }}
            response['{{ underscored_pluralized_entity_name }}'][key].blobinfo = \
                    {
                        "content_type": {{ underscored_entity_name }}.blobinfo.content_type,
                        "creation": {{ underscored_entity_name }}.blobinfo.creation,
                        "size": {{ underscored_entity_name }}.blobinfo.size,
                        "filename": {{ underscored_entity_name }}.blobinfo.filename
                    }

        return self.response.out.write(json.dumps(response, cls=JsonEncoder))
# }}}

# GetUploadUrl {{{
class GetUploadUrl(webapp.RequestHandler):
    """Return an object with all the {{ readable_noncapitalized_pluralized_entity_name }} objects
    """
    def get(self):
        from google.appengine.ext import blobstore

        return self.response.out.write(json.dumps({"upload_url": blobstore.create_upload_url('/{{ underscored_entity_name }}/create/')}, cls=JsonEncoder))
# }}}

# Remove {{{
class Remove(webapp.RequestHandler):
    """Retrun a {{ readable_noncapitalized_entity_name }} object 
    """
    def get(self):
        status, object = _get_path_{{ underscored_entity_name }}(self.request.path)

        if status != 200:
            self.response.set_status(status)
            return self.response.out.write(json.dumps(object, cls=JsonEncoder))
        else:
            {{ underscored_entity_name }} = object # just to improve readability

        {{ underscored_entity_name }}.blobinfo.delete()

        {{ underscored_entity_name }}.delete()

        return self.response.out.write(json.dumps({}, cls=JsonEncoder))
# }}}

# Create {{{
class Create(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        {{ underscored_entity_name }} = {{ camelcased_entity_name }}()

        fields = {{ underscored_entity_name }}.fields()
        for key in self.request.POST:
            if key in fields:
                setattr({{ underscored_entity_name }}, key, self.request.POST[key])

        # check whether there is already file using this permalink
        result =\
            {{ camelcased_entity_name }}\
                .all()\
                .filter("permalink", {{ underscored_entity_name }}.permalink)\
                .fetch(1)

        # set blobinfo {{{
        upload_files = self.get_uploads('file')  # 'file' is file upload field in the form
        if len(upload_files) == 0:
            # prompt failure
            return self.redirect('/{{ underscored_entity_name }}/failure/Please Choose a file')

        blobinfo = upload_files[0]
        {{ underscored_entity_name }}.blobinfo = blobinfo.key()
        # }}}

        if len(result) != 0:
            # remove uploaded blob
            blobinfo.delete()

            # prompt failure
            return self.redirect('/{{ underscored_entity_name }}/failure/Permalink Already Exists')

        {{ underscored_entity_name }}.created_by = users.User()
        {{ underscored_entity_name }}.modified_by = users.User()

        {{ underscored_entity_name }}.put()

        self.redirect('/{{ underscored_entity_name }}/success/')
# }}}

# Failure {{{
class Failure(webapp.RequestHandler):
    def get(self):
        return self.response.out.write("Failure")
# }}}

# Success {{{
class Success(webapp.RequestHandler):
    def get(self):
        return self.response.out.write("Success")
# }}}

# Default {{{
class Default(blobstore_handlers.BlobstoreDownloadHandler):
    """Default serves the paths we don't have particular mapping for
    """
    def get(self):
        permalink = self.request.path.replace('/{{ underscored_entity_name }}/', '');

        result =\
            {{ camelcased_entity_name }}\
                .all()\
                .filter("permalink", permalink)\
                .fetch(1)

        if len(result) == 0:
            return self.error(404)

        for {{ underscored_entity_name }} in result:
            return self.send_blob({{ underscored_entity_name }}.blobinfo)
# }}}

# init application {{{
application = webapp.WSGIApplication([
    ('/{{ underscored_entity_name }}/all/', All),
    ('/{{ underscored_entity_name }}/create/', Create),
    ('/{{ underscored_entity_name }}/get_upload_url/', GetUploadUrl),
    ('/{{ underscored_entity_name }}/success/', Success),
    ('/{{ underscored_entity_name }}/failure/.*', Failure),
    ('/{{ underscored_entity_name }}/[^/]*/remove/', Remove),
    ('.*', Default),
], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
# }}}

# vim:fdm=marker:fmr={{{,}}}:
