#!/usr/bin/env python

import os
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template

BASE_URL = 'http://ogori-masu.appspot.com'

class Recording(db.Model):
    """Captures the Twilio POST sent when recording completes."""

    call_sid = db.StringProperty(required=True)
    caller = db.StringProperty(required=True)
    url = db.StringProperty(required=True)
    date = db.DateTimeProperty(auto_now_add=True)
    played = db.BooleanProperty(default=False)

    @staticmethod
    def get_next():
        """Returns the URL of the next recording to be played."""
        query = Recording.gql('WHERE played = :1 ORDER BY date ASC', False)

        recording = query.get()

        if recording is not None:
            recording.played = True
            recording.put()
            return recording

        return None

class MainPage(webapp.RequestHandler):
    """Plays a message if one exists, then <Record>s a new one."""
    def post(self):
        template_values = {
                'recording': Recording.get_next(),
                'action': BASE_URL + '/record'
                }

        if self.request.get('format') == 'json':
            import json
            self.response.out.write(json.dumps(template_values))
        else:
            path = os.path.join(os.path.dirname(__file__), 'response.xml')
            self.response.headers['Content-Type'] = 'text/xml'
            self.response.out.write(template.render(path, template_values))

class RecordPage(webapp.RequestHandler):
    """Saves the URL of the recorded message."""
    def post(self):
        call_sid = self.request.get('CallSid')
        caller = self.request.get('From')
        url = self.request.get('RecordingUrl')

        Recording(call_sid=call_sid, caller=caller, url=url).put()

application = webapp.WSGIApplication([
    ('/', MainPage),
    ('/record', RecordPage)
], debug=True)

def main():
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
