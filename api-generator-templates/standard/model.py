#!/usr/bin/env python

from apis.models import {{ project_underscored_name }}_data_models
from google.appengine.ext import db

class {{ camelcased_entity_name }}({{ project_underscored_name }}_data_models.{{ project_camel_cased_name }}Expando):
    # Attributes {{{
    {% @properties %}
    {{ item.underscored_name }} = {{ item.model_definition }}
    {% /@properties %}
    # }}}

# vim:fdm=marker:fmr={{{,}}}:
