from datetime import date
from datetime import datetime
from datetime import time
import json
try:
   import urllib.parse
except:
   import urllib

from rest_framework import exceptions

class BackupService:

    def __init__(self):
        import logging
        self.logger = logging.getLogger(__name__)

    def create(self, * args, ** kwargs):
        self.logger.info("Start setting BackupRequest Attributes before creation")
        #print('CREATE')
        backup = kwargs.pop("backup")
        backup.modified = datetime.now()
        url = '/SearchSvc/CVWebService.svc/Backupset'
        host = '10.5.254.43'
        headers = 'application/xml'
        #get token
        Authtoken = ''
        params = '<App_CreateBackupSetRequest><association><entity><appName>Virtual Server</appName><backupsetName>' + backup.name + '</backupsetName><clientName>client001</clientName><instanceName>' + backup.server + '</instanceName><subclientName>default</subclientName></entity></association></App_CreateBackupSetRequest>';
        self.logger.info('url='+url+',params='+repr(params))
        headers={"Content-Type": "application/xml", "Accept": "application/xml", "Authtoken" : Authtoken}
        import requests
        response = requests.post(url, headers=headers, data=params, verify=False)
        status = response.status_code
        content = response.text
        logger.info('status='+repr(status)+' content=' + repr(content))
        if ((str(response.status_code) == '200') or (str(response.status_code) == '201')):
           #content = '<?xml version="1.0" encoding="UTF-8" standalone="no" ?><App_GenericResponse><response errorCode="0"><entity _type_="ROOT_ENTITY" applicationId="33" backupsetId="931" clientId="2" clientSidePackage="true" consumeLicense="true" srmReportSet="0" srmReportType="0" type="GALAXY"/></response></App_GenericResponse>'
           import xml.etree.ElementTree as ET
           root = ET.fromstring(content)
           e = root.findall(".//entity")
           if 'backupsetId' in e[0].attrib:
             print("BackupSetId: " + e[0].attrib["backupsetId"])
             backup.location = e[0].attrib["backupsetId"]
        else:
           raise exceptions.MethodNotAllowed(method='create', detail='Backup server returned:' + str(content))
        self.logger.info("End setting BackupRequest Attributes before creation")

    def delete(self, * args, ** kwargs):
        self.logger.info("Start setting BackupRequest Attributes before delete")
        #print('DELETE')
        backup = kwargs.pop("backup")
        backup.modified = datetime.now()
        url = '/SearchSvc/CVWebService.svc/Backupset/' + backup.location
        host = '10.5.254.43'
        headers = 'application/xml'
        #get token
        Authtoken = ''
        import requests
        response = requests.post(url, headers=headers, data=params, verify=False)
        status = response.status_code
        content = response.text
        logger.info('status='+repr(status)+' content=' + repr(content))
        if ((str(response.status_code) == '200') or (str(response.status_code) == '201')):
           self.logger.info(repr(content))
           '<App_GenericResponse><response errorCode="0"/></App_GenericResponse>'
        else:
           raise exceptions.MethodNotAllowed(method='create', detail='Backup server returned:' + str(content))
        self.logger.info("End setting BackupRequest Attributes before delete")

    def update(self, * args, ** kwargs):
        self.logger.info("Start setting BackupRequest Attributes before modify")
        #print('MODIFY')
        backup = kwargs.pop("backup")
        backup.modified = datetime.now()
        self.logger.info("End setting BackupRequest Attributes before modify")
