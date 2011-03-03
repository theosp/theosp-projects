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

        return self.response.out.write(json.dumps(response, cls=JsonEncoder))
# }}}

# Get {{{
class Get(webapp.RequestHandler):
    """Retrun a {{ readable_noncapitalized_entity_name }} object 
    """
    def get(self):
        status, object = _get_path_{{ underscored_entity_name }}(self.request.path)

        if status != 200:
            self.response.set_status(status)
            return self.response.out.write(json.dumps(object, cls=JsonEncoder))
        else:
            {{ underscored_entity_name }} = object # just to improve readability

        return self.response.out.write(json.dumps({{ underscored_entity_name }}, cls=JsonEncoder))
# }}}

# Create {{{
class Create(webapp.RequestHandler):
    """Create a new {{ readable_noncapitalized_entity_name }}
    """

    def post(self):
        {{ underscored_entity_name }} = {{ camelcased_entity_name }}()

        query = json.loads(self.request.POST['query'])

        fields = {{ underscored_entity_name }}.fields()
        for key in query:
            if key in fields:
                setattr({{ underscored_entity_name }}, key, query[key])

        {{ underscored_entity_name }}.created_by = users.User()
        {{ underscored_entity_name }}.modified_by = users.User()

        {{ underscored_entity_name }}.put()

        return self.response.out.write(json.dumps({'{{ underscored_entity_name }}_key': str({{ underscored_entity_name }}.key())}, cls=JsonEncoder))
# }}}

# Save {{{
class Save(webapp.RequestHandler):
    """Edit existing one
    """
    def post(self):
        status, object = _get_path_{{ underscored_entity_name }}(self.request.path)

        if status != 200:
            self.response.set_status(status)
            return self.response.out.write(json.dumps(object, cls=JsonEncoder))
        else:
            {{ underscored_entity_name }} = object # just to improve readability

        query = json.loads(self.request.POST['query'])

        fields = {{ underscored_entity_name }}.fields()
        for key in query:
            if key in fields:
                setattr({{ underscored_entity_name }}, key, query[key])

        {{ underscored_entity_name }}.modified_by = users.User()

        {{ underscored_entity_name }}.put()

        return self.response.out.write(json.dumps({}, cls=JsonEncoder))
# }}}

# Default {{{
class Default(webapp.RequestHandler):
    """Default serves the paths we don't have particular mapping for
    """
    def get(self):
        if self.request.path[-1] != '/':
            return self.redirect(self.request.path + '/', permanent=True)

        self.error(404)
# }}}

# init application {{{
application = webapp.WSGIApplication([
    ('/{{ underscored_entity_name }}/all/', All),
    ('/{{ underscored_entity_name }}/create/', Create),
    ('/{{ underscored_entity_name }}/[^/]*/save/', Save),
    ('/{{ underscored_entity_name }}/[^/]*/', Get),
    ('.*', Default),
], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
# }}}

# vim:fdm=marker:fmr={{{,}}}:
