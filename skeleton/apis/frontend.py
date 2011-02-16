#!/usr/bin/env python

###########################################################
# Solve bug: http://groups.google.com/group/google-appengine-python/browse_thread/thread/e3a9d8b8be36870d/5dc96ab56b889dc6?pli=1
# Remove the standard version of Django and put version 1.1
import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from appengine_django import InstallAppengineHelperForDjango
InstallAppengineHelperForDjango(version='1.1')
###########################################################

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

from urlparse import urlparse

import os


class GetFrontend(webapp.RequestHandler):
    """Default serves the paths we don't have particular mapping for
    """

    def get(self):
        url = self.request.path
        parsed_url = urlparse(url)
        path = parsed_url.path

        if path == '/' or path == '':
            frontend = 'home'
        else:
            frontend = path.split('/')[1]

        frontend_template_path = os.path.join(os.path.dirname(__file__), '..', 'frontends', frontend + '.html')

        return self.response.out.write(template.render(frontend_template_path, {}))

application = webapp.WSGIApplication([
    ('.*', GetFrontend),
], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
