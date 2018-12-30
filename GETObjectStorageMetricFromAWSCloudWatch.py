# Copyright 2010-2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# ADAPATED TO GET ON-PREMISE OBJECT STORAGE METRICS BY Ravi Rajamani
#
# This file is licensed under the Apache License, Version 2.0 (the "License").
# You may not use this file except in compliance with the License. A copy of the
# License is located at
#
# http://aws.amazon.com/apache2.0/
#
# This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS
# OF ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.

# AWS Version 4 signing example

# Monitoring API (Monitoring)

# See: http://docs.aws.amazon.com/general/latest/gr/sigv4_signing.html
# This version makes a POST request and passes request parameters
# in the body (payload) of the request. Auth information is passed in
# an Authorization header.
import sys, os, base64, datetime, hashlib, hmac
import requests # pip install requests

# ************* REQUEST VALUES *************
method = 'POST'
service = os.environ.get('AWS_service')
host = os.environ.get('AWS_host')
region = os.environ.get('AWS_region')
endpoint = os.environ.get('AWS_endpoint')
request_parameters = os.environ.get('AWS_request_parameters')
apiName='GetMetricStatistics'
# PUT requests use a content type header. For Monitoring API,
# the content is JSON.
content_type = 'application/x-amz-json-1.0'
# Monitoring API requires an x-amz-target header
amz_target = 'GraniteServiceVersion20100801.'+apiName

# Request parameters for CreateTable--passed in a JSON block.
t = datetime.datetime.utcnow()
request_parameters = '{'
request_parameters += '    "Action": "GetMetricStatistics", '
request_parameters += '    "Namespace": "On-PremiseObjectStorageMetrics",'
request_parameters += '    "MetricName": "BucketSizeBytes ",'
request_parameters += '    "Dimensions": ['
request_parameters += '        {'
request_parameters += '            "Name": "BucketName",'
request_parameters += '            "Value": "ExampleBucket"'
request_parameters += '        }'
request_parameters += '    ],'
request_parameters += '    "StartTime": 1545884562,'
request_parameters += '    "EndTime":  1545884662,'
#request_parameters += '    "StartTime": 2018-12-25T23:00:00Z,'
#request_parameters += '    "EndTime": 2018-12-27T23:00:00Z,'
request_parameters += '    "Period": 86400,'
request_parameters += '    "Statistics": ['
request_parameters += '        "Average"'
request_parameters += '    ],'
request_parameters += '    "Unit": "Bytes"'
request_parameters += '}'
"""
request_parameters = '{'
request_parameters += '"Dimensions.member.1.Value": "ExampleBucket", '
request_parameters += '"MetricName": "BucketSizeBytes", '
request_parameters += '"Period": 86400, '
request_parameters += '"Version": "2010-08-01",'
request_parameters += '"Statistics.member.1": "Average",'
request_parameters += '"EndTime": 2018-12-27T23:00:00Z,'
request_parameters += '"StartTime": 2018-12-25T23:00:00Z,'
request_parameters += '"Dimensions.member.1.Name": "BucketName",'
request_parameters += '"Action": "GetMetricStatistics",'
request_parameters += '"Namespace": "On-PremiseObjectStorageMetrics"'
request_parameters += '}'
"""
print(request_parameters)


# Key derivation functions. See:
# http://docs.aws.amazon.com/general/latest/gr/signature-v4-examples.html#signature-v4-examples-python
def sign(key, msg):
    return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()

def getSignatureKey(key, date_stamp, regionName, serviceName):
    kDate = sign(('AWS4' + key).encode('utf-8'), date_stamp)
    kRegion = sign(kDate, regionName)
    kService = sign(kRegion, serviceName)
    kSigning = sign(kService, 'aws4_request')
    return kSigning

# Read AWS access key from env. variables or configuration file. Best practice is NOT
# to embed credentials in code.
access_key = os.environ.get('AWS_ACCESS_KEY_ID')
secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
if access_key is None or secret_key is None:
    print('No access key is available.')
    sys.exit()

# Create a date for headers and the credential string
amz_date = t.strftime('%Y%m%dT%H%M%SZ')
date_stamp = t.strftime('%Y%m%d') # Date w/o time, used in credential scope


# ************* TASK 1: CREATE A CANONICAL REQUEST *************
# http://docs.aws.amazon.com/general/latest/gr/sigv4-create-canonical-request.html

# Step 1 is to define the verb (GET, POST, etc.)--already done.

# Step 2: Create canonical URI--the part of the URI from domain to query
# string (use '/' if no path)
canonical_uri = '/'

## Step 3: Create the canonical query string. In this example, request
# parameters are passed in the body of the request and the query string
# is blank.
canonical_querystring = ''

# Step 4: Create the canonical headers. Header names must be trimmed
# and lowercase, and sorted in code point order from low to high.
# Note that there is a trailing \n.
canonical_headers = 'content-type:' + content_type + '\n' + 'host:' + host + '\n' + 'x-amz-date:' + amz_date + '\n' + 'x-amz-target:' + amz_target + '\n'

# Step 5: Create the list of signed headers. This lists the headers
# in the canonical_headers list, delimited with ";" and in alpha order.
# Note: The request can include any headers; canonical_headers and
# signed_headers include those that you want to be included in the
# hash of the request. "Host" and "x-amz-date" are always required.
signed_headers = 'content-type;host;x-amz-date;x-amz-target'

# Step 6: Create payload hash. In this example, the payload (body of
# the request) contains the request parameters.
payload_hash = hashlib.sha256(request_parameters.encode('utf-8')).hexdigest()

# Step 7: Combine elements to create canonical request
canonical_request = method + '\n' + canonical_uri + '\n' + canonical_querystring + '\n' + canonical_headers + '\n' + signed_headers + '\n' + payload_hash


# ************* TASK 2: CREATE THE STRING TO SIGN*************
# Match the algorithm to the hashing algorithm you use, either SHA-1 or
# SHA-256 (recommended)
algorithm = 'AWS4-HMAC-SHA256'
credential_scope = date_stamp + '/' + region + '/' + service + '/' + 'aws4_request'
string_to_sign = algorithm + '\n' +  amz_date + '\n' +  credential_scope + '\n' +  hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()

# ************* TASK 3: CALCULATE THE SIGNATURE *************
# Create the signing key using the function defined above.
signing_key = getSignatureKey(secret_key, date_stamp, region, service)

# Sign the string_to_sign using the signing_key
signature = hmac.new(signing_key, (string_to_sign).encode('utf-8'), hashlib.sha256).hexdigest()


# ************* TASK 4: ADD SIGNING INFORMATION TO THE REQUEST *************
# Put the signature information in a header named Authorization.
authorization_header = algorithm + ' ' + 'Credential=' + access_key + '/' + credential_scope + ', ' +  'SignedHeaders=' + signed_headers + ', ' + 'Signature=' + signature

# "x-amz-target", "content-type", and "Authorization". Except for the authorization
# header, the headers must be included in the canonical_headers and signed_headers values, as
# noted earlier. Order here is not significant.
# # Python note: The 'host' header is added automatically by the Python 'requests' library.
#headers = {'Content-Type':content_type,
#           'X-Amz-Date':amz_date,
#           'X-Amz-Target':amz_target,
#           'Authorization':authorization_header}
headers = {'x-amz-date':amz_date,
           'Authorization':authorization_header,
           'x-amz-target':'GraniteServiceVersion20100801.'+apiName,
           'Content-Type': content_type,
           'Accept': 'application/json',
           'Content-Encoding': 'amz-1.0',
           'Connection': 'keep-alive'}



# ************* SEND THE REQUEST *************
print('\nBEGIN REQUEST++++++++++++++++++++++++++++++++++++')
print('Request URL = ' + endpoint)

r = requests.post(endpoint, data=request_parameters, headers=headers)

print('\nRESPONSE++++++++++++++++++++++++++++++++++++')
print('Response code: %d\n' % r.status_code)
print(r.text)


"""
{    "Action": "GetMetricStatistics",     "Namespace": "On-PremiseObjectStorageMetrics",    "MetricName": "BucketSizeBytes ",    "Dimensions": [        {            "Name": "BucketName",            "Value": "ExampleBucket"        }    ],    "StartTime": 1545884562,    "EndTime":  1545884662,    "Period": 86400,    "Statistics": [        "Average"    ],    "Unit": "Bytes"}

BEGIN REQUEST++++++++++++++++++++++++++++++++++++
Request URL = https://monitoring.us-east-1.amazonaws.com

RESPONSE++++++++++++++++++++++++++++++++++++
Response code: 200

{"Datapoints":[],"Label":"BucketSizeBytes "}
aws cloudwatch get-metric-statistics --metric-name BucketSizeBytes --start-time 2018-12-25T23:00:00 --end-time 2018-12-27T23:00:00 --period 86400 --namespace On-PremiseObjectStorageMetrics --statistics Average --dimensions Name=BucketName,Value=ExampleBucket
{
    "Label": "BucketSizeBytes",
    "Datapoints": [
        {
            "Timestamp": "2018-12-26T23:00:00Z",
            "Average": 1024000000000.0,
            "Unit": "Bytes"
        }
    ]
}
"""
