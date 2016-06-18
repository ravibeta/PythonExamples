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

    def test_create_model(self):
        print('start test create model')
        self.client = APIClient()
        self.url = '/backup/v1/exports' #reverse('backup-create')
        self.client.force_authenticate(user=None)
        response = self.client.post(self.url, {
                   "name": "sj1010005254041-Backup1",
                   "region":"us-west-1",
                   "platform":"VMWare",
                   "server": "sj1010005254041.corp.adobe.com",
                   "owner": "somebody"})
        print('response='+repr(response.content))
        self.assertEqual(str(response.status_code), "201") #status.HTTP_200_OK
        self.url = reverse('backup-list')
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url, {"hostname": "sj1010005254041.corp.adobe.com"})
        print('response='+repr(response.content))
        import json
        items = json.loads(response.content.decode("utf-8"))
        print(items)
        self.assertEqual(items["count"], 1)
        self.assertTrue(items["results"][0]["location"] != "")
        print('end test create model')

    def test_delete_model(self):
        print('start test delete model')
        self.test_create_model()
        self.client = APIClient()
        self.url = '/backup/v1/exports' #reverse('backup-create')
        self.client.force_authenticate(user=None)
        self.url = reverse('backup-list')
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url, {"hostname": "sj1010005254041.corp.adobe.com"})
        print('response='+repr(response.content))
        import json
        items = json.loads(response.content.decode("utf-8"))
        print(items)
        self.assertEqual(items["count"], 1)
        id = items["results"][0]["id"]
        self.assertTrue(int(id) > 0)
        response = self.client.delete(self.url+ "/"+str(id))
        print('response='+repr(response.content))
        self.assertEqual(str(response.status_code), "204") #status.HTTP_200_OK
        self.url = reverse('backup-list')
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url, {"hostname": "sj1010005254041.corp.adobe.com"})
        print('response='+repr(response.content))
        import json
        items = json.loads(response.content.decode("utf-8"))
        print(items)
        self.assertEqual(items["count"], 0)
        print('end test delete model')
