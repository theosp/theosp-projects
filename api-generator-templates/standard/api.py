#!/usr/bin/env python

from google.appengine.dist import use_library
use_library('django', '1.2')

# imports {{{
from google.appengine.ext import webapp, db
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

from lib import simplejson as json

from google.appengine.api import users

from apis import registered_user

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
        callback = self.request.GET.get('callback') or ""

        page_size = int(page_size)
        page = int(page)

        {{ underscored_pluralized_entity_name }}_query = {{ camelcased_entity_name }}.all().order(order_by)

        registered_user.add_user_group_filter({{ underscored_pluralized_entity_name }}_query)

        paged_query = PagedQuery({{ underscored_pluralized_entity_name }}_query, page_size)

        results = paged_query.fetch_page(page)
        pages_count = paged_query.page_count()

        response = {'{{ underscored_pluralized_entity_name }}': [], 'pager': {'pages_count': pages_count}}
        for {{ underscored_entity_name }} in results:
            response["{{ underscored_pluralized_entity_name }}"].append(\
                {"key": str({{ underscored_entity_name }}.key()),\
                 {% @properties %}
                 "{{ item.underscored_name }}": {{ underscored_entity_name }}.{{ item.underscored_name }},\
                 {% /@properties %}
                })

        response = json.dumps(response, cls=JsonEncoder)

        if callback != "":
            response = callback + "(" + response + ")"

        return self.response.out.write(response)
# }}}

# Get {{{
class Get(webapp.RequestHandler):
    """Retrun a {{ readable_noncapitalized_entity_name }} object 
    """
    def get(self):
        status, object = _get_path_{{ underscored_entity_name }}(self.request.path)

        if not registered_user.user_in_entity_group(object):
            self.response.set_status(403)
            return self.response.out.write("Permission Denied")

        if status != 200:
            self.response.set_status(status)
            return self.response.out.write(json.dumps(object, cls=JsonEncoder))
        else:
            {{ underscored_entity_name }}_object = object # just to improve readability

        response_obejct = {}
        for field in {{ underscored_entity_name }}_object.fields():
            response_obejct[field] = getattr({{ underscored_entity_name }}_object, field)

        {% @properties %}
        {% !item.trivial_conversion_of_list_items_types_python %}
        response_obejct["{{ item.underscored_name }}"] =\
                [str(item) for item in response_obejct["{{ item.underscored_name }}"]]
        {% /!item.trivial_conversion_of_list_items_types_python %}
        {% /@properties %}

        return self.response.out.write(json.dumps(response_obejct, cls=JsonEncoder))
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
            {% !some_properties_need_special_treatment_after_json_decode %}
            if key in fields:
                setattr({{ underscored_entity_name }}, key, query[key])
            {% /!some_properties_need_special_treatment_after_json_decode %}
            {% ?some_properties_need_special_treatment_after_json_decode %}
            if key in fields:
                {% @properties %}
                {% !item.trivial_conversion_of_list_items_types_python %}
                if key == "{{ item.underscored_name }}":
                    {{ underscored_entity_name }}.{{ item.underscored_name }} = \
                            [db.Key(item) for item in query["{{ item.underscored_name }}"]]
                else:
                    setattr({{ underscored_entity_name }}, key, query[key])
                {% /!item.trivial_conversion_of_list_items_types_python %}
                {% /@properties %}
            {% /?some_properties_need_special_treatment_after_json_decode %}

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

        if not registered_user.user_in_entity_group({{ underscored_entity_name }}):
            self.response.set_status(403)
            return self.response.out.write("Permission Denied")

        query = json.loads(self.request.POST['query'])

        fields = {{ underscored_entity_name }}.fields()
        for key in query:
            {% !some_properties_need_special_treatment_after_json_decode %}
            if key in fields:
                setattr({{ underscored_entity_name }}, key, query[key])
            {% /!some_properties_need_special_treatment_after_json_decode %}
            {% ?some_properties_need_special_treatment_after_json_decode %}
            if key in fields:
                {% @properties %}
                {% !item.trivial_conversion_of_list_items_types_python %}
                if key == "{{ item.underscored_name }}":
                    {{ underscored_entity_name }}.{{ item.underscored_name }} = \
                            [db.Key(item) for item in query["{{ item.underscored_name }}"]]
                else:
                    setattr({{ underscored_entity_name }}, key, query[key])
                {% /!item.trivial_conversion_of_list_items_types_python %}
                {% /@properties %}
            {% /?some_properties_need_special_treatment_after_json_decode %}

        try:
            {{ underscored_entity_name }}.modified_by = users.User()
        except users.UserNotFoundError:
            {{ underscored_entity_name }}.modified_by = None

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
