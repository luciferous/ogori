#!/usr/bin/env python

from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

BASE_URL = 'http://ogori-masu.appspot.com'

class Recording(db.Model):
    """Captures the Twilio POST sent when recording completes."""

    call_sid = db.StringProperty(required=True)
    caller = db.StringProperty(required=True)
    url = db.StringProperty(required=True)
    date = db.DateTimeProperty(auto_now_add=True)
    played = db.BooleanProperty()

    @staticmethod
    def get_next():
        """Returns the URL of the next recording to be played."""
        query = Recording.gql('WHERE played = :1 ORDER BY date ASC', False)

        recording = query.get()

        if recording not None:
            recording.played = True
            recording.put()
            return recording

        return None

class MainPage(webapp.RequestHandler):
    """Plays a message if one exists, then <Record>s a new one."""
    def post(self):
        self.response.out.write(
                '<?xml version="1.0" encoding="UTF-8"?><Response>')
        rec = Recording.get_next()
        if rec is not None:
            self.response.out.write('<Play>%s</Play>' % rec.url)
        url = BASE_URL + '/record'
        self.response.out.write('''\
                <Record action="%s"/>
                </Response>''' % url
                )

class RecordPage(webapp.RequestHandler):
    """Saves the URL of the recorded message."""
    def post(self):
        call_sid = self.request.post('CallSid')
        caller = self.request.post('From')
        url = self.request.post('RecordingUrl')

        Recording(call_sid=call_sid, caller=caller, url=url).put()

application = webapp.WSGIApplication([
    ('/', MainPage),
    ('/record', RecordPage)
], debug=True)

def main():
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
