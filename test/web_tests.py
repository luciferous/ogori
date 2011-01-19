import unittest
from webtest import TestApp
from google.appengine.ext import db
from google.appengine.ext import webapp
import ogori

class PlayTest(unittest.TestCase):

    def test_get_next_recording(self):
        entity = ogori.Recording(recording_url='foo')
        entity.put()

        conf = webapp.WSGIApplication([('/', ogori.MainPage)], debug=True)
        app = TestApp(conf)
        response = app.post('/')
        self.assertEqual('200 OK', response.status)

