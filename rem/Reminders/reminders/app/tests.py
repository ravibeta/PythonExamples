from __future__ import unicode_literals
from django.test import TestCase, RequestFactory
from datetime import datetime, date, time
from reminders import settings
#import settings
import app.views

import json
import base64
import uuid

try:
    import urllib.parse as urllib
except ImportError:
    import urllib

from django.core.urlresolvers import reverse
from django.views.generic import View

class ModelTestCase(TestCase):
    def test_view(self):
        print 'executing test case'
        reminder_request_data = {'term':1, 'email':'rajamani@adobe.com', 'purpose': 'test', 'landscape':'Dev'}
        auth_headers = {
        }
        #response = self.client.post('http://10.5.250.38:8388/lease/v1/leases', data=reminder_request_data, **auth_headers)
        response = self.client.post(reverse('home'), data=reminder_request_data, **auth_headers)
        print('post returned'+repr(response.content))
        self.assertEqual(response.status_code, 200)
        #r = json.loads(response.content.decode("utf-8"))
        self.assertTrue('Success' in repr(response.content))
        self.assertTrue(True)

    def test_reminder(self):
        self.test_view()
        #check expiration time
        auth_headers = {
        }
        import requests
        response = requests.get('http://10.5.250.38:8388/lease/v1/leases', headers=auth_headers)
        print('get returned'+repr(response.content))

    def test_qrcode(self):
        self.test_view()
        self.factory = RequestFactory()
        auth_headers = {
        }
        request = self.factory.get("/qrcode?ID=1", **auth_headers)
        response = app.views.getQRCode(request)
        self.assertTrue('.bmp' in repr(response.content))

    def test_list(self):
        self.factory = RequestFactory()
        auth_headers = {
        }
        request = self.factory.get("/list/", **auth_headers)
        response = app.views.reminder_list(request)
        items = json.loads(response)
        self.assertTrue(len(items) > 0)

    def test_delete(self):
        self.factory = RequestFactory()
        auth_headers = {
        }
        request = self.factory.get("/list/", **auth_headers)
        response = app.views.reminder_delete(request)
        self.assertTrue('Reminder deleted successfully' in  str(response))

    def test_delete(self):
        self.factory = RequestFactory()
        auth_headers = {
        }
        request = self.factory.get("/list/", **auth_headers)
        response = app.views.reminder_edit(request)
        self.assertTrue('Reminder deleted successfully' in  str(response))

def testThis():
    t = ModelTestCase()
    t.test_model()
