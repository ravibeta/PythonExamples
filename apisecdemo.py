#!flask/bin/python
import flask
from flask import Flask, jsonify
from OpenSSL import SSL
from flask import make_response
from flask import Flask, Blueprint
from flask import request
import urlparse
import logging
from hashlib import sha224
from functools import wraps
import base64
import hmac
import hashlib
import time

app = Flask(__name__)

@app.errorhandler(Exception)
def all_exception_handler(error):
   return make_response(jsonify({'error': 'Bad request'}), 400)


import urllib2

def authenticate():
    message = {'message': "Authenticate."}
    app.logger.info(str(message))
    resp = jsonify(message)
    resp.status_code = 401
    resp.headers['WWW-Authenticate'] = 'Basic realm="Example"'
    return resp

def requires_auth(f):
    theurl = 'https://127.0.0.1:5000/list'
    key = "YPUOPPLRO1HZ" # ''.join([random.choice(string.digits + string.ascii_uppercase) for x in range(0, 12)])
    secret = "77238733AEBA6D89" #''.join([random.choice('0123456789ABCDEF') for x in range(0, 16)])
    passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
    # this creates a password manager
    passman.add_password(None, theurl, key, secret)
    authhandler = urllib2.HTTPBasicAuthHandler(passman)
    # create the AuthHandler
    opener = urllib2.build_opener(authhandler)
    urllib2.install_opener(opener)

    app.logger.info('requires_auth')
    app.logger.info(str(f))
    @wraps(f)
    def decorated(*args, **kwargs):
        app.logger.info('decorated')
        app.logger.info(str(request.headers))
        auth = request.headers['Authorization']
        if not auth:
           return authenticate()
        if not check_auth(auth):
           app.logger('check_auth failed')
           return authenticate()
        return f(*args, **kwargs)
    return decorated

# use authHandler = urllib.request.HTTPBasicAuthHandler(manager)
def check_auth(auth):
    app.logger.info(auth)
    AccessKeyId = "YPUOPPLRO1HZ" # ''.join([random.choice(string.digits + string.ascii_uppercase) for x in range(0, 12)])
    Secret = "77238733AEBA6D89" #''.join([random.choice('0123456789ABCDEF') for x in range(0, 16)])
    HMAC_KEY =  Secret.decode('hex')
    timestamp = request.args.get('timestamp',str(time.time()).split('.')[0])
    token = request.args.get('token', '000000')
    CanonicalizedResource = 'timestamp=' + timestamp + '&' + 'token=' + str(token)
    StringToSign = CanonicalizedResource
    expectedSignature = base64.b64encode(
        hmac.new(
            HMAC_KEY,
            StringToSign,
            hashlib.sha256
            ).digest()
        )
    expectedDigest = bytearray(expectedSignature)
    actualSignature = str(auth.replace(str("Basic " + " " + AccessKeyId + ":" ), ""))
    actualDigest = bytearray(actualSignature)
    app.logger.info(actualSignature + "\n" + expectedSignature + "\n")
    return actualSignature == expectedSignature
    return compare_digest(actualDigest, expectedDigest)

def requires_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('apiToken')
        if not token:
           return authenticate()
        if not check_token(token):
           return authenticate()
        return f(*args, **kwargs)
    return decorated

def check_token(f):
    """ To be implemented """
    return TRUE

def compare_digest(x, y):
    if not (isinstance(x, bytes) and isinstance(y, bytes)):
        raise TypeError("both inputs should be instances of bytes")
    if len(x) != len(y):
        return False
    result = 0
    for a, b in zip(x, y):
        result |= a ^ b
    return result == 0

@app.route('/list', methods=['GET'])
@requires_auth
def list():
     return jsonify({'msg': 'welcome', 'success':'success'}), 200

ADMINS = ['rravishankar@gmail.com']
if not app.debug:
    import logging
    from logging.handlers import SMTPHandler
    mail_handler = SMTPHandler('127.0.0.1',
                               'server-error@foo.com',
                               ADMINS, 'API Failed! ')
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)

if __name__ == '__main__':
    app.run(debug=True, port=8999)
