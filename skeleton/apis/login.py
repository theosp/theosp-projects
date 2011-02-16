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
from google.appengine.api import users

import os
from urlparse import urlparse

class OpenIdLoginHandler(webapp.RequestHandler):
    def get(self):
        continue_url = self.request.GET.get('continue') or \
                       'http://' + urlparse(self.request.url).hostname + '/admin'
        openid_url = self.request.GET.get('openid') or \
                     self.request.GET.get('openid_identifier')

        if not openid_url:
            path = os.path.join(os.path.dirname(__file__), 'templates', 'login.html')

            self.response.out.write(template.render(path, {'continue': continue_url}))
        else:
            self.redirect(users.create_login_url(continue_url, None, openid_url))

application = webapp.WSGIApplication([
    ('/_ah/login_required', OpenIdLoginHandler),
], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
