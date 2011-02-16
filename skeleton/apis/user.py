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

from google.appengine.api import users

from lib import simplejson as json

class JsonEncoder(json.JSONEncoder):
    def default(self, obj):
        """Example for type encoder definition

        if isinstance(obj, date):
            return '**new Date(%i,%i,%i)' % (obj.year,
                                             obj.month-1,
                                             obj.day)
        """

        return obj.__dict__

# Default serves the paths we don't have particular mapping for
class Default(webapp.RequestHandler):
    def get(self):
        if self.request.path[-1] != '/':
            return self.redirect(self.request.path + '/', permanent=True)

        self.error(404)

# Me returns the current user's User object
class Me(webapp.RequestHandler):
    def get(self):
        try:
            user = users.User()
        except users.UserNotFoundError:
            user_object = {
                'logged': False
            }
        else:
            user_object = {
                'logged': True,
                'federated_identity': user.federated_identity(),
                'federated_provider': user.federated_provider(),
                'email': user.email(),
                'admin': users.is_current_user_admin(),
                'logout_url': users.create_logout_url('/')
            }

        return self.response.out.write(json.dumps(user_object, cls=JsonEncoder))

application = webapp.WSGIApplication([
    ('/user/me/', Me),
    ('.*', Default),
], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
