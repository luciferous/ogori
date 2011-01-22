import unittest
from webtest import TestApp
from google.appengine.ext import db
from google.appengine.ext import webapp
import ogori

class PlayTest(unittest.TestCase):

    def test_get_next_recording(self):
        first = ogori.Recording(url='foo', call_sid='123', caller='123')
        first.put()
        second = ogori.Recording(url='bar', call_sid='123', caller='123')
        second.put()

        self.assertEqual(False, first.played)
        self.assertEqual(False, second.played)

        conf = webapp.WSGIApplication([('/', ogori.MainPage)], debug=True)
        app = TestApp(conf)
        response = app.post('/')
        self.assertEqual('200 OK', response.status)

        rec1 = ogori.Recording.get(first.key())
        self.assertEqual(True, rec1.played)

        rec2 = ogori.Recording.get(second.key())
        self.assertEqual(False, rec2.played)

    def test_record_handler(self):
        conf = webapp.WSGIApplication(
                [('/record', ogori.RecordPage)],
                debug=True
                )
        app = TestApp(conf)
        response = app.post('/record', {
            'CallSid': '123',
            'From': '321',
            'RecordingUrl': 'http://example.com/play/me.mp3'
            })

        self.assertEqual('200 OK', response.status)

        rec = ogori.Recording.get_next()
        self.assertEqual('123', rec.call_sid)
        self.assertEqual('321', rec.caller)
        self.assertEqual('http://example.com/play/me.mp3', rec.url)

    def test_no_recording(self):
        conf = webapp.WSGIApplication([('/', ogori.MainPage)], debug=True)
        app = TestApp(conf)
        response = app.post('/', 'format=json')

        import json
        result = json.loads(response.body)
        self.assertEquals(None, result['recording'])
        self.assertEquals(
                'http://ogori-masu.appspot.com/record',
                result['action']
                )

