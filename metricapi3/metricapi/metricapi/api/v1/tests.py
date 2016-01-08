from __future__ import unicode_literals
from django.test import TestCase, RequestFactory
from datetime import datetime, date, time
from metricapi import settings

import json
import base64
import uuid

try:
    import urllib.parse as urllib
except ImportError:
    import urllib

from django.core.urlresolvers import reverse
from django.views.generic import View

class SharedTestMixin(object):
    def getMetrics(self):
        response = self.client.get(reverse('metric-list'))
        self.assertEqual(response.status_code, 200)
        self.results = json.loads(response.content.decode("utf-8"))
        print(getReminders.__name__+' results = ' + repr(self.result))

class ModelTestCase(TestCase, SharedTestMixin):

    def setUp(self):
        if hasattr(self, 'init') and self.init:
            return
        self.id = 0
        self.factory = RequestFactory()
        self.init = True
        self.results = []

    def test_model(self):
        self.assertTrue(True)

    def test_create_reminder(self):
        reminder_request_data = {'term':1, 'email':'rajamani@adobe.com'}
        auth_headers = {
        }
        response = self.client.post('/add', data=reminder_request_data, **auth_headers)
        print('post returned'+repr(response.content))
        self.assertEqual(response.status_code, 200)
        r = json.loads(response.content.decode("utf-8"))
        print('create returned'+repr(r))
        self.assertTrue(int(r['metricid']) > 0)
    

def testThis():
    t = ModelTestCase()
    t.test_model()

