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
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import memcache

class FlushAll(webapp.RequestHandler):
    def get(self):
        memcache.flush_all()

        return self.response.out.write('Memcache Flushed')

class Default(webapp.RequestHandler):
    """Default serves the paths we don't have particular mapping for
    """

    def get(self):
        if self.request.path[-1] != '/':
            return self.redirect(self.request.path + '/', permanent=True)

        self.error(404)

application = webapp.WSGIApplication([
    (r'/memcache/flush_all/?', FlushAll),
    (r'.*', Default),
], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
