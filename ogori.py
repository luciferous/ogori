#!/usr/bin/env python

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

class MainPage(webapp.RequestHandler):
    """Plays a message if one exists, then <Record>s a new one."""
    pass

class RecordPage(webapp.RequestHandler):
    """Saves the URL of the recorded message."""
    pass

application = webapp.WSGIApplication([
    ('/', MainPage),
    ('/record', RecordPage)
], debug=True)

def main():
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
