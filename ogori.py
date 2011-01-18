#!/usr/bin/env python

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

BASE_URL = 'http://ogori-masu.appspot.com'
class MainPage(webapp.RequestHandler):
    """Plays a message if one exists, then <Record>s a new one."""
    def get(self):
        self.response.out.write(
                '<?xml version="1.0" encoding="UTF-8"?><Response>')
        rec = Recording.get_next()
        if rec is not None:
            self.response.out.write('<Play>%s</Play>' % rec.recording_url)
        url = BASE_URL + '/record'
        self.response.out.write('''\
                <Record action="%s"/>
                </Response>''' % url
                )

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
