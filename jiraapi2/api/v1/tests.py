from rest_framework.test import APIRequestFactory
from django.core.urlresolvers import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
#from api.v1.models.jira import JiraRequest
#from cloudapi_utils import user
from jiraapi import settings
import json
from django.contrib.auth.models import User

class JiraTestCase(TestCase): 

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

    def createDB(self):
        result = self.invokeDBCmd('CREATE TABLE api_jirarequest(`id` INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,`receiver` VARCHAR(128) NOT NULL,`sender`  VARCHAR(128) NOT NULL,`cc`  VARCHAR(128),`bcc`  VARCHAR(128),`subject`  VARCHAR(128),`message`  VARCHAR(128),`digest_hash` VARCHAR(128) NOT NULL,`user_name` VARCHAR(128),`created` datetime DEFAULT NULL,`modified` datetime NOT NULL,`status` VARCHAR(8) NOT NULL);')
        print('DB ret = '+ repr(result))
        pass

    def setUp(self):
        self.createDB()
        self.factory = APIRequestFactory()
        print('in main setup')
        pass

    def tearDown(self):
        print('in main test tearDown')

    """
    def testsend(self):
        self.url = reverse('messages-list')
        print('reverse='+self.url)
        request = self.factory.get(self.url)
        view =  JiraRequestViewSet.as_view()
        response = view.request()
        jira = Jira()
    """

    def test_list_shares(self):
        print('start test_list_shares')
        #user = User.objects.get(email='rajamani@adobe.com')
        self.client = APIClient()
        self.url = '/jira/v1/messages/'
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)
        print('response='+repr(response.content))
        self.assertEqual(str(response.status_code), "200") #status.HTTP_200_OK
