from rest_framework.test import APIRequestFactory
from django.core.urlresolvers import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
#from api.v1.models.backup import BackupRequest
#from cloudapi_utils import user
from commvaultapi import settings
import json
from django.contrib.auth.models import User

class BackupTestCase(TestCase):
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
        output = process.communicate(bytes(command + "\n", "ascii"))[0]
        msg =  'DB returned='+str(output)
        print(msg)
        return output

    def setUp(self):
        self.id = 0
        self.count = 0
        self.name = "djangotestshare"
        if self.count < 1:
           self.count += 1
           lines = []
           with open("api/v1/tables_create.sql", "r") as myfile:
              for line in myfile:
                  output = self.invokeDBCmd(line)
                  print(str(output))

    def test_create_backup(self):
        print('start test create backup')
        self.client = APIClient()
        self.url = '/backup/v1/create'
        self.client.force_authenticate(user=None)
        response = self.client.post(self.url, {"hostname": "foo.com"})
        print('response='+repr(response.content))
        self.assertEqual(str(response.status_code), "200") #status.HTTP_200_OK
        print('end test create backup')

    def test_delete_backup(self):
        print('start test delete backup')
        self.client = APIClient()
        self.url = '/backup/v1/delete'
        self.client.force_authenticate(user=None)
        response = self.client.post(self.url, {"hostname": "foo.com"})
        print('response='+repr(response.content))
        self.assertEqual(str(response.status_code), "200") #status.HTTP_200_OK
        print('end test delete backup')
