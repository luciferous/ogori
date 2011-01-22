import unittest

from google.appengine.ext import db
import ogori

class RecordingTest(unittest.TestCase):

    def test_get_next_recording(self):
        ogori.Recording(url='foo', call_sid='123', caller='123').put()
        ogori.Recording(url='bar', call_sid='456', caller='456').put()

        rec = ogori.Recording.get_next()
        self.assertEquals('foo', rec.url)

        rec = ogori.Recording.get_next()
        self.assertEquals('bar', rec.url)
