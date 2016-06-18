# -*- Mode:Python; indent-tabs-mode:nil; tab-width:4 -*-
#
#
# This file could be part of duplicity.
#
# meant to be used as follows:
# duplicity "https://vcd-sj/9-0.vmdk?dcPath=sj1&dsName=0058" file:///local/mybackup
#
# remember to keep config.ini in the same folder as this file.
# Duplicity is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version.
#
# Duplicity is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with duplicity; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

import base64
import httplib, os
import httplib2
import sys
import re
import urllib
import urllib2
import xml.dom.minidom
import json
from urllib import quote_plus #python3 is not supported

import duplicity.backend
from duplicity import globals
from duplicity import log
from duplicity.errors import * #@UnusedWildImport
from duplicity import urlparse_2_5 as urlparser
from duplicity.backend import retry_fatal

class CustomMethodRequest(urllib2.Request):
    """
    This request subclass allows explicit specification of
    the HTTP request method. Basic urllib2.Request class
    chooses GET or POST depending on self.has_data()
    """
    def __init__(self, method, *args, **kwargs):
        self.method = method
        urllib2.Request.__init__(self, *args, **kwargs)

    def get_method(self):
        return self.method

class vCenterBackend(): ##duplicity.backend.Backend):
    def __init__(self, parsed_url):
        ##duplicity.backend.Backend.__init__(self, parsed_url)
        self.headers = {} ##{'Connection': 'keep-alive'}
        self.parsed_url = parsed_url

        try:
            from ConfigParser import RawConfigParser
        except:
            from configparser import RawConfigParser

        parser = RawConfigParser()
        parser.read('config.ini')
        VCOSERVERURL = self.parsed_url.split('/')[2] #parser.get('vco', 'server_url')
        print('VCOSERVERURL='+VCOSERVERURL)
        self.hostname = VCOSERVERURL
        VCOAUTH = parser.get('vco', 'http_auth')
        VCOUSER = parser.get('vco', 'vco_user')
        VCOPWD = parser.get('vco', 'vco_pwd')



        self.username = VCOUSER
        self.password =  VCOPWD
        self.headers['Authorization'] = self.get_authorization()
        self.directory = self.getfolder1(parsed_url) #self._sanitize_path(parsed_url.path)
        self.scheme = self.parsed_url.split('/')[0][:-1]
        if 'https' in self.scheme:
           self.port = 443
        else:
           self.port = 80
        self.conn = None

    def _sanitize_path(self,path):
        if path:
            foldpath = re.compile('/+')
            return foldpath.sub('/', path + '/' )
        else:
            return '/'

    def _getText(self,nodelist):
        rc = ""
        for node in nodelist:
            if node.nodeType == node.TEXT_NODE:
                rc = rc + node.data
        return rc
    
    def _connect(self, forced=False):
        """
        Connect or re-connect to the server, updates self.conn
        # reconnect on errors as a precaution, there are errors e.g. 
        # "[Errno 32] Broken pipe" or SSl errors that render the connection unusable
        """
        #if self.retry_count<=1 and self.conn \
        #    and self.conn.host == self.parsed_url.hostname: return
        
        print("HTTPS vCenter create connection on '%s' " % (self.hostname) )
        if self.conn: self.conn.close()
        # http schemes needed for redirect urls from servers
        if self.scheme in ['vcenter','http']:
            self.conn = httplib.HTTPConnection(self.hostname, self.port)
        elif self.scheme in ['vcenter','https']:
            if True: #globals.ssl_no_check_certificate:
                ##self.conn = httplib.HTTPSConnection(self.hostname, self.port)
                ##print('conn='+repr(self.conn))
                ##self.http = httplib2.Http(".cache", disable_ssl_certificate_validation=True)
                ##print('http='+repr(self.http))
                ##self.http.add_credentials(self.username, self.password)
                pass
            else:
               raise FatalBackendError("vCenter verified ssl certificate not supported: %s" % (self.scheme))
        else:
            raise FatalBackendError("vCenter Unknown URI scheme: %s" % (self.scheme))

    def close(self):
        self.conn.close()

    def request(self, method, path, data=None, redirected=0):
        """
        Wraps the connection.request method to retry once if authentication is
        required
        """
        self._connect()
        quoted_path = urllib.quote(path,"/:~")
        self.headers['Authorization'] = self.get_authorization()

        print("vCenter %s %s request with headers: %s " % (method,quoted_path,self.headers))
        print("vCenter data length: %s " % len(str(data)) )
        url = path ##url = vcoserver +  path
        params =  ''
        if data != None:
            params = data
        print ('params='+repr(params))
        #params = {"dsName": "HDS005_CORP_0058",
        #          "dcPath": "sj1"}
        sys.stdout.flush()
        #import ssl
        #context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        #context.verify_mode = ssl.CERT_NONE
        #service_instance = SmartConnect(host=host,user=vcouser,pwd=vcopwd,port=port,sslContext=context)
        #print('service_instance='+repr(service_instance))
        #if not service_instance:
        #    raise Exception("Could not connect to the specified host using specified "
        #          "username and password")
        #atexit.register(Disconnect, service_instance)
        #cookie = self.make_compatible_cookie(service_instance._stub.cookie)
        #import requests
        #response = requests.get(url, headers=self.headers, verify=False, stream=True)
        #print(response.status_code)
        #print(r.text)
        #print(r.status_code)
        #'''
        ###response, content = self.http.request(url,method, headers=self.headers, body=json.dumps(params)) #cookies=cookie)
        ###print('response=' + repr(response))
        ###print('content=' + repr(content))
        ###if ((response.status != 200) and (response.status != 201)):
        ###   raise FatalBackendError("vCenter missing location header in redirect response.")
        #'''
        #self.conn.request(method, quoted_path, data, self.headers)
        #response = self.conn.getresponse()
        #print("vCenter response status %s with content '%s'." % (response.status,content))
        # resolve redirects and reset url on listing requests (they usually come before everything else)
        """
            request = requests.put(folderurl,
                                   params=params,
                                   data=f,
                                   headers=headers,
                                   cookies=cookie,
                                   verify=False)
        """
        return response


    def get_authorization(self, response=None, path=None):
        return self.get_basic_authorization()

    def get_basic_authorization(self):
        """
        Returns the basic auth header
        """
        auth_string = '%s:%s' % (self.username, self.password)
        return 'Basic %s' % base64.encodestring(auth_string).strip()

    @retry_fatal
    def _list(self):
        """List files in directory"""
        print("Listing directory %s on vCenter server" % (self.directory,))
        pass

    def makedir(self):
        pass

    def make_compatible_cookie(client_cookie):
        cookie_name = client_cookie.split("=", 1)[0]
        cookie_value = client_cookie.split("=", 1)[1].split(";", 1)[0]
        cookie_path = client_cookie.split("=", 1)[1].split(";", 1)[1].split(";", 1)[0].lstrip()
        cookie_text = " " + cookie_value + "; $" + cookie_path
        # Make a cookie
        cookie = dict()
        cookie[cookie_name] = cookie_text
        return cookie
    
    def getfolder1(self, url):
        print(url)
        url = url[0:url.index("vse", url.index("vse")+1)] + url[url.index("?"):]
        return url

    def makeurl(self, url, item):
        url = url[0:url.index("vse", url.index("vse")+1)] + item + url[url.index("?"):]
        print('makeurl='+url)
        return url
    
    def getcontents(self, url):
        modurl = self.getfolder1(url)
        print(modurl)
        headers = {'Authorization': get_authorization()}
        import requests
        r = requests.get(modurl, headers=headers, verify=False)
        print(r.text)
        print(r.status_code)
        pattern = "<a href=\""
        urls = []
        if pattern in r.text:
            i = r.text.index(pattern)
            while (i != -1):
                  href = r.text[r.text.find(">",i+len(pattern))+1:r.text.find("<", i+len(pattern)+1)]
                  print(href)
                  urls.append(self.makeurl(url,quote_plus(href)))
                  i = r.text.find(pattern, i+1)
        print(urls)
        return urls


    def __taste_href(self, href):
        """
        Internal helper to taste the given href node and, if
        it is a duplicity file, collect it as a result file.

        @return: A matching filename, or None if the href did not match.
        """
        raw_filename = self._getText(href.childNodes).strip()
        parsed_url = urlparser.urlparse(urllib.unquote(raw_filename))
        filename = parsed_url.path
        log.Debug("vCenter path decoding and translation: "
                  "%s -> %s" % (raw_filename, filename))

        if filename.startswith(self.directory):
            filename = filename.replace(self.directory,'',1)
            return filename
        else:
            return None

    def genCode(self):
        import random
        import string
        return ''.join([random.choice(string.digits + string.ascii_uppercase) for x in range(0, 12)])
    
    ##@retry_fatal
    def get(self, remote_filename, local_path):
        """Get remote filename, saving it to local_path"""
        print('parsed_url='+self.parsed_url)
        url = self.makeurl(self.parsed_url, remote_filename)
        print("Retrieving %s from vCenter server" % (url))
        response = None
        try:
            #target_file = open(local_path, "wb+") ##
            #response = self.request("GET", url)
            import requests
            print('HEADERSSSS='+repr(self.headers))
            print('url='+repr(url))
            response = requests.get(url,
                                   #params='',
                                   headers=self.headers,
                                   #cookies=cookie,
                                   verify=False,
                                   stream=True)
            written=[]
            local_filename = self.genCode()
            with open(os.path.join(local_path, local_filename), "wb") as f:
                 count = 0
                 for chunk in response.iter_content(chunk_size=1024):
                     if chunk: # filter out keep-alive new chunks
                         f.write(chunk)
                         count = (count + 1)  % 1024000
                         print('count='+str(count))
                         if count > 5:
                            break
            written.append(local_filename)
            #if response.status == 200:
                #data=response.read()
                #target_file.write(response.read())
                #import hashlib
                #print("vCenter GOT %s bytes with md5=%s" % (len(data),hashlib.md5(data).hexdigest()) )
                #assert not target_file.close()
                #local_path.setdata()
                ##response.close()
            #else:
            #    status = response.status
            #    reason = response.reason
            #    response.close()
            #    raise BackendException("Bad status code %s reason %s." % (status,reason))
        except Exception, e:
            raise e
        finally:
            ##if response: response.close()
            pass

    @retry_fatal
    def put(self, source_path, remote_filename = None):
        """Transfer source_path to remote_filename"""
        if not remote_filename:
            remote_filename = source_path.get_filename()
        url = self.directory + remote_filename
        print("Saving %s on vCenter server" % (url ,))
        response = None
        try:
            source_file = source_path.open("rb")
            response = self.request("PUT", url, source_file.read())
            if response.status in [201, 204]:
                response.read()
                response.close()
            else:
                status = response.status
                reason = response.reason
                response.close()
                raise BackendException("Bad status code %s reason %s." % (status,reason))
        except Exception, e:
            raise e
        finally:
            if response: response.close()

    @retry_fatal
    def delete(self, filename_list):
        """Delete files in filename_list"""
        """
            import requests
            request = requests.delete(folderurl,
                                   params=params,
                                   data=f,
                                   headers=headers,
                                   cookies=cookie,
                                   verify=False)
        """
        for filename in filename_list:
            url = self.directory + filename
            print("Deleting %s from vCenter server" % (url ,))
            response = None
            try:
                response = self.request("DELETE", url)
                if response.status == 204:
                    response.read()
                    response.close()
                else:
                    status = response.status
                    reason = response.reason
                    response.close()
                    raise BackendException("Bad status code %s reason %s." % (status,reason))
            except Exception, e:
                raise e
            finally:
                if response: response.close()

#duplicity.backend.register_backend("vcenter", vCenterBackend)
