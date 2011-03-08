#!/usr/bin/env python

from google.appengine.ext import db

class {{ camelcased_entity_name }}(db.Expando):
    # Attributes {{{
    name = db.StringProperty(default="New {{ readable_capitalized_entity_name }}")

    {% @properties %}
    {{ item.name }} = {{ item.model_definition }}
    {% /@properties %}

    # Modifications date tracking {{{
    date_created = db.DateTimeProperty(auto_now_add=True)
    date_modified = db.DateTimeProperty(auto_now=True)
    # }}}

    # Created/modified by {{{
    created_by = db.UserProperty()
    modified_by = db.UserProperty()
    # }}}

# vim:fdm=marker:fmr={{{,}}}:
