# import relevant libraries
import base64
import json
import urllib
import httplib2
import hmac
import binascii
import hashlib
import random
import time
from Crypto.Cipher import AES


http = httplib2.Http(".cache", disable_ssl_certificate_validation=True)

# setup

AccessKeyId = "YPUOPPLRO1HZ" # ''.join([random.choice(string.digits + string.ascii_uppercase) for x in range(0, 12)])
Secret = "77238733AEBA6D89" #''.join([random.choice('0123456789ABCDEF') for x in range(0, 16)])
from totp import OneTimePasswordAlgorithm
otp = OneTimePasswordAlgorithm()
t = time.time()
timestamp = str(t).split('.')[0]
token = otp.generateTOTP(Secret, timestamp, '6', hashlib.sha256)
import email.utils as eut
# to timestamp HTTP header
dt = eut.formatdate(timeval=t, localtime=False, usegmt=True)

#strategy

#Authorization =  " " + AccessKeyId + ":" + Signature;
#Signature = Base64( HMAC-SHA256( YourSecretAccessKeyID, UTF-8-Encoding-Of( StringToSign ) ) );
#StringToSign = 'timestamp=' + timestamp + '&' + 'token=' + str(token)

HMAC_KEY =  Secret.decode('hex')

# implementation
CanonicalizedResource = 'timestamp=' + timestamp + '&' + 'token=' + str(token)
StringToSign = CanonicalizedResource
Signature = base64.b64encode(
        hmac.new(
            HMAC_KEY,
            StringToSign,
            hashlib.sha256
            ).digest()
        )
auth = " " + AccessKeyId + ":" + Signature
print 'auth=' + auth
host = '127.0.0.1'
port = '8999'
url = 'http://' + host + ':' + port + '/list' + '?' + CanonicalizedResource
# get
#http.add_credentials(api_user, api_pwd)
response,content = http.request(url,
 headers={'Authorization' : 'Basic ' + auth, 'Date' : str(dt)})
print content
data = json.loads(content)
if not data["success"] :
   raise Error('bad request')
