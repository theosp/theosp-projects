#!/usr/bin/env python

from google.appengine.dist import use_library
use_library('django', '1.2')

# imports {{{
from google.appengine.ext import webapp, db
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

from lib import simplejson as json
from django.utils.datastructures import SortedDict

from google.appengine.api import users

from apis import registered_user

from urlparse import urlparse

import os

from apis.models.{{ underscored_entity_name }} import {{ camelcased_entity_name }}
from apis.helpers.paging import PagedQuery

from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers

from google.appengine.api.datastore_errors import EntityNotFoundError
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
        result =\
            {{ camelcased_entity_name }}\
                .all()\
                .filter("permalink", {{ underscored_entity_name }}_key)\
                .fetch(1)

        if len(result) == 0:
            return (400, "Couldn't find a {{ readable_noncapitalized_entity_name }} with a key or permalink: `%s'" % {{ underscored_entity_name }}_key)
        else:
            {{ underscored_entity_name }} = result[0]

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
        callback = self.request.GET.get('callback') or ""

        page = int(page)
        page_size = int(page_size)

        {{ underscored_pluralized_entity_name }}_query = {{ camelcased_entity_name }}.all().order(order_by)

        registered_user.add_user_group_filter({{ underscored_pluralized_entity_name }}_query)

        paged_query = PagedQuery({{ underscored_pluralized_entity_name }}_query, page_size)

        results = paged_query.fetch_page(page)
        pages_count = paged_query.page_count()

        response = {'{{ underscored_pluralized_entity_name }}': [], 'pager': {'pages_count': pages_count}}
        for {{ underscored_entity_name }} in results:
            try:
                {{ underscored_entity_name }} = {
                    "key": str({{ underscored_entity_name }}.key()),
                    "permalink": {{ underscored_entity_name }}.permalink,
                    "group": {{ underscored_entity_name }}.group,
                    "modified_by": {{ underscored_entity_name }}.modified_by,
                    "created_by": {{ underscored_entity_name }}.created_by,
                    "date_created": {{ underscored_entity_name }}.date_created,
                    "date_modified": {{ underscored_entity_name }}.date_modified,
                    "blobinfo": {
                        "content_type": {{ underscored_entity_name }}.blobinfo.content_type,
                        "creation": {{ underscored_entity_name }}.blobinfo.creation,
                        "size": {{ underscored_entity_name }}.blobinfo.size,
                        "filename": {{ underscored_entity_name }}.blobinfo.filename
                    }
                }
            except EntityNotFoundError:
                import logging
                logging.error("Entity not found on {{ underscored_pluralized_entity_name }} fs: key: `%s'; permalink: `%s'" % (media_file.key(), media_file.permalink))
                continue

            response["{{ underscored_pluralized_entity_name }}"].append({{ underscored_entity_name }})

        response = json.dumps(response, cls=JsonEncoder)

        if callback != "":
            response = callback + "(" + response + ")"

        return self.response.out.write(response)
# }}}

# GetUploadUrl {{{
class GetUploadUrl(webapp.RequestHandler):
    """Return an object with all the {{ readable_noncapitalized_pluralized_entity_name }} objects
    """
    def get(self):
        from google.appengine.ext import blobstore

        callback = self.request.GET.get('callback') or ""

        response = json.dumps({"upload_url": blobstore.create_upload_url('/{{ underscored_entity_name }}/create/')}, cls=JsonEncoder)

        if callback != "":
            response = callback + "(" + response + ")"

        return self.response.out.write(response)
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

        if not registered_user.user_in_entity_group({{ underscored_entity_name }}):
            self.response.set_status(403)
            return self.response.out.write("Permission Denied")

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

        {{ underscored_entity_name }}.permalink = {{ underscored_entity_name }}.permalink.strip()

        if len({{ underscored_entity_name }}.permalink) == 0:
            return self.redirect('/{{ underscored_entity_name }}/failure/You have to pick a permalink')

        # set blobinfo {{{
        upload_files = self.get_uploads('file')  # 'file' is file upload field in the form
        if len(upload_files) == 0:
            # prompt failure
            return self.redirect('/{{ underscored_entity_name }}/failure/Please Choose a file')

        blobinfo = upload_files[0]
        {{ underscored_entity_name }}.blobinfo = blobinfo.key()
        # }}}

        # check whether there is already file using this permalink {{{
        result =\
            {{ camelcased_entity_name }}\
                .all()\
                .filter("permalink", {{ underscored_entity_name }}.permalink)\
                .fetch(1)

        if len(result) != 0:
            # remove uploaded blob
            blobinfo.delete()

            # prompt failure
            return self.redirect('/{{ underscored_entity_name }}/failure/Permalink Already Exists')
        # }}}

        {% ?mime_types_restriced %}
        # check whether mimetype allowed {{{
        if blobinfo.content_type not in [{% @allowed_mime_types %}"{{ . }}"{% !last %}, {% /!last %}{% /@allowed_mime_types %}]:
            # remove uploaded blob
            blobinfo.delete()

            # prompt failure
            return self.redirect('/{{ underscored_entity_name }}/failure/File Type ' + blobinfo.content_type + ' Not Allowed')
        # }}}
        {% /?mime_types_restriced %}

        try:
            {{ underscored_entity_name }}.created_by = users.User()
        except users.UserNotFoundError:
            {{ underscored_entity_name }}.created_by = None

        try:
            {{ underscored_entity_name }}.modified_by = users.User()
        except users.UserNotFoundError:
            {{ underscored_entity_name }}.modified_by = None

        registered_user.apply_user_group_to_entity({{ underscored_entity_name }})
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
