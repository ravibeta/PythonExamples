from __future__ import unicode_literals
from django.test import TestCase, RequestFactory
from datetime import datetime, date, time
from leaseapi import settings

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
    def getReminders(self):
        response = self.client.get(reverse('lease-list'))
        self.assertEqual(response.status_code, 200)
        self.results = json.loads(response.content.decode("utf-8"))
        print(getReminders.__name__+' results = ' + repr(self.result))

class ModelTestCase(TestCase, SharedTestMixin):
    def invokeDBCmd(self, command):
        host = settings.DATABASES["default"]["HOST"]
        port = settings.DATABASES["default"]["PORT"]
        user = settings.DATABASES["default"]["USER"]
        password = settings.DATABASES["default"]["PASSWORD"]
        db = settings.DATABASES["default"]["NAME"]
        from subprocess import Popen, PIPE
        process = Popen(['mysql', '--host='+host, '--port='+port, '--database='+db,
                 '--connect-timeout=60', '--user='+user, '-p'+password],
                 stdout=PIPE, stdin=PIPE)
        output = process.communicate(command)[0] #bytes(command + "\n", "ascii"))[0]
        msg =  'DB returned='+str(output)
        return output


    def setUp(self):
        if hasattr(self, 'init') and self.init:
            return
        self.id = 0
        self.count = 0
        if self.count < 1:
           self.count += 1
           lines = []
           with open("create_tables.sql", "r") as myfile:
              for line in myfile:
                  output = self.invokeDBCmd(line)
        self.factory = RequestFactory()
        self.init = True
        self.results = []

    def test_model(self):
        self.assertTrue(True)

    def test_extended_request(self):
        self.factory = RequestFactory()
        token_request_data = {
        }
        auth_headers = {
        }
        response = self.client.get(reverse('lease-list'))
        self.assertEqual(response.status_code, 200)
        print(repr(response.content))

        #request = self.request_factory.get("/fake-req", **auth_headers)
        #request.user = "fake"
        self.assertTrue(True)

    def test_create_reminder(self):
        reminder_request_data = {'term':1, 'email':'rajamani@adobe.com'}
        auth_headers = {
        }
        response = self.client.post(reverse('lease-list'), data=reminder_request_data, **auth_headers)
        print('post returned'+repr(response.content))
        self.assertEqual(response.status_code, 200)
        r = json.loads(response.content.decode("utf-8"))
        print('create returned'+repr(r))
        self.assertTrue(int(r['leaseid']) > 0)
    
    def test_unsubscribe(self):
        response = self.client.get(reverse('lease-list'))
        self.assertEqual(response.status_code, 200)
        self.results = json.loads(response.content.decode("utf-8"))
        if not self.results or len(self.results) < 1:
               self.test_create_reminder()
        response = self.client.get(reverse('lease-list'))
        self.assertEqual(response.status_code, 200)
        self.results = json.loads(response.content.decode("utf-8"))
        leaseid = self.results[0]['id']
        guid = self.results[0]['resource']['guid']
        print('guid='+guid)
        reminder_request_data = { 'leaseid':leaseid , 'guid':uuid.UUID('{'+guid+'}')}
        auth_headers = {
        }
        response = self.client.post(reverse('unsubscribe'), data=json.dumps(reminder_request_data), **auth_headers)
        print('unsubscribe returned'+repr(response.content))
        self.assertEqual(response.status_code, 200)

    def test_unlease(self):
        response = self.client.get(reverse('lease-list'))
        self.assertEqual(response.status_code, 200)
        self.results = json.loads(response.content.decode("utf-8"))
        if not self.results or len(self.results) < 1:
               self.test_create_reminder()
        response = self.client.get(reverse('lease-list'))
        self.assertEqual(response.status_code, 200)
        self.results = json.loads(response.content.decode("utf-8"))
        print('before unlease' + repr(self.results))
        leaseid = self.results[0]['id']
        guid = self.results[0]['resource']['guid']
        reminder_request_data = { 'leaseid':leaseid , 'guid':uuid.UUID('{'+guid+'}')}
        auth_headers = {
        }
        response = self.client.post(reverse('unlease'), data=json.dumps(reminder_request_data), **auth_headers)
        print('unlease returned'+repr(response.content))
        self.assertEqual(response.status_code, 200)

    def test_delete_reminder(self):
        response = self.client.get(reverse('lease-list'))
        self.assertEqual(response.status_code, 200)
        self.results = json.loads(response.content.decode("utf-8"))
        if not self.results or len(self.results) < 1:
               self.test_create_reminder()
        response = self.client.get(reverse('lease-list'))
        self.assertEqual(response.status_code, 200)
        self.results = json.loads(response.content.decode("utf-8"))
        auth_headers = {
        }
        url = reverse('lease-list')
        print('url='+str(url))
        response = self.client.delete(str(url)+'/1', **auth_headers)
        print('delete returned'+repr(response.content))
        self.assertEqual(response.status_code, 200)
        

def testThis():
    t = ModelTestCase()
    t.test_model()

