package com.emc.ecs.s3.sample;
import java.io.UnsupportedEncodingException;
import java.security.InvalidKeyException;
import java.security.NoSuchAlgorithmException;

import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class GetMetricsRequest {
    private static final Logger logger = LoggerFactory.getLogger(GetMetricsRequest.class);

    public static byte[] computeHmacSHA256(byte[] key, String data) throws NoSuchAlgorithmException, InvalidKeyException, IllegalStateException,
            UnsupportedEncodingException {
        String algorithm = "HmacSHA256";
        String charsetName = "UTF-8";

        Mac sha256_HMAC = Mac.getInstance(algorithm);
        SecretKeySpec secret_key = new SecretKeySpec(key, algorithm);
        sha256_HMAC.init(secret_key);

        return sha256_HMAC.doFinal(data.getBytes(charsetName));
    }

    public static byte[] computeHmacSHA256(String key, String data) throws NoSuchAlgorithmException, InvalidKeyException, IllegalStateException,
            UnsupportedEncodingException {
        return computeHmacSHA256(key.getBytes(), data);
    }

    public static String getSignatureV4(String accessSecretKey, String date, String region, String regionService, String signing, String stringToSign)
            throws InvalidKeyException, NoSuchAlgorithmException, IllegalStateException, UnsupportedEncodingException {

        byte[] dateKey = computeHmacSHA256(accessSecretKey, date);
        logger.debug("dateKey: {}", encodeToString(dateKey));

        byte[] dateRegionKey = computeHmacSHA256(dateKey, region);
        logger.debug("dateRegionKey: {}", encodeToString(dateRegionKey));

        byte[] dateRegionServiceKey = computeHmacSHA256(dateRegionKey, regionService);
        logger.debug("dateRegionServiceKey: {}", encodeToString(dateRegionServiceKey));

        byte[] signingKey = computeHmacSHA256(dateRegionServiceKey, signing);
        logger.debug("signingKey: {}", encodeToString(signingKey));

        byte[] signature = computeHmacSHA256(signingKey, stringToSign);
        logger.debug("signature: {}", encodeToString(signature));

        return encodeToString(signature);
    }
    private static final char[] DIGITS = {
            '0', '1', '2', '3', '4', '5', '6', '7',
            '8', '9', 'a', 'b', 'c', 'd', 'e', 'f'
    };
    public static String encodeToString(byte[] bytes) {
        char[] encodedChars = encode(bytes);
        return new String(encodedChars);
    }
    public static char[] encode(byte[] data) {

        int l = data.length;

        char[] out = new char[l << 1];

        // two characters form the hex value.
        for (int i = 0, j = 0; i < l; i++) {
            out[j++] = DIGITS[(0xF0 & data[i]) >>> 4];
            out[j++] = DIGITS[0x0F & data[i]];
        }

        return out;
    }
    protected static int toDigit(char ch, int index) throws IllegalArgumentException {
        int digit = Character.digit(ch, 16);
        if (digit == -1) {
            throw new IllegalArgumentException("Illegal hexadecimal character " + ch + " at index " + index);
        }
        return digit;
    }
    protected static byte[] HmacSHA256(String data, byte[] key) throws Exception {
        String algorithm="HmacSHA256";
        Mac mac = Mac.getInstance(algorithm);
        mac.init(new SecretKeySpec(key, algorithm));
        return mac.doFinal(data.getBytes("UTF8"));
    }

    protected static byte[] getSignatureKey(String key, String dateStamp, String regionName, String serviceName) throws Exception {
        byte[] kSecret = ("AWS4" + key).getBytes("UTF8");
        byte[] kDate = HmacSHA256(dateStamp, kSecret);
        byte[] kRegion = HmacSHA256(regionName, kDate);
        byte[] kService = HmacSHA256(serviceName, kRegion);
        byte[] kSigning = HmacSHA256("aws4_request", kService);
        return kSigning;
    }

    public static void main(String[] args) throws InvalidKeyException, NoSuchAlgorithmException, IllegalStateException, UnsupportedEncodingException {
        String AWS_ACCESS_KEY_ID="MY_ACCESS_KEY";
        String AWS_SECRET_ACCESS_KEY="MY_SECRET_KEY";
        String service="monitoring";
        String host="monitoring.us-east-1.amazonaws.com";
        String region="us-east-1";
        String endpoint="https://monitoring.us-east-1.amazonaws.com";
        String AWS_request_parameters="Action=GetMetricStatistics&Version=2010-08-01";
        String amz_date = "20181230T125500Z";
        String date_stamp = "20181230";
        String canonical_uri = "/";
        String canonical_querystring = "";
        String method = "POST";
        String apiName = "GetMetricStatistics";
        String content_type = "application/x-amz-json-1.0";
        String amz_target = "GraniteServiceVersion20100801."+apiName;
        String canonical_headers = "content-type:" + content_type + "\n" + "host:" + host + "\n" + "x-amz-date:" + amz_date + "\n" + "x-amz-target:" + amz_target + "\n";
        String signed_headers = "content-type;host;x-amz-date;x-amz-target";
          String accessKey = AWS_ACCESS_KEY_ID;
          String accessSecretKey = AWS_SECRET_ACCESS_KEY;
          String date = "20130806";
          String signing = "aws4_request";
        String request_parameters = "{";
        request_parameters += "    \"Action\": \"GetMetricStatistics\", ";
        request_parameters += "    \"Namespace\": \"On-PremiseObjectStorageMetrics\",";
        request_parameters += "    \"MetricName\": \"BucketSizeBytes \",";
        request_parameters += "    \"Dimensions\": [";
        request_parameters += "        {";
        request_parameters += "            \"Name\": \"BucketName\",";
        request_parameters += "            \"Value\": \"ExampleBucket\"";
        request_parameters += "        }";
        request_parameters += "    ],";
        request_parameters += "    \"StartTime\": 1545884562,";
        request_parameters += "    \"EndTime\":  1545884662,";
        request_parameters += "    \"Period\": 86400,";
        request_parameters += "    \"Statistics\": [";
        request_parameters += "        \"Average\"";
        request_parameters += "    ],";
        request_parameters += "    \"Unit\": \"Bytes\"";
        request_parameters += "}";

        // String payload_hash = hashlib.sha256(request_parameters.encode('utf-8')).hexdigest()
        // String canonical_request = method + '\n' + canonical_uri + '\n' + canonical_querystring + '\n' + canonical_headers + '\n' + signed_headers + '\n' + payload_hash;
        // String algorithm = 'AWS4-HMAC-SHA256';
        // String credential_scope = date_stamp + '/' + region + '/' + service + '/' + 'aws4_request';
        // String string_to_sign = algorithm + '\n' +  amz_date + '\n' +  credential_scope + '\n' +  hashlib.sha256(canonical_request.encode('utf-8')).hexdigest();
        // String signing_key = getSignatureKey(secret_key, date_stamp, region, service);
        // String signature = hmac.new(signing_key, (string_to_sign).encode('utf-8'), hashlib.sha256).hexdigest();
        // String authorization_header = algorithm + ' ' + 'Credential=' + access_key + '/' + credential_scope + ', ' +  'SignedHeaders=' + signed_headers + ', ' + 'Signature=' + signature;
        // logger.info("signature: {}", getSignatureV4(accessSecretKey, date, region, regionService, signing, request_parameters));
        try {
            byte[] signing_key = getSignatureKey(accessSecretKey, date_stamp, region, service);
            logger.info("signature: {}", encodeToString(signing_key));
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

}
//
// output:
// [main] INFO com.emc.ecs.s3.sample.GetMetricsRequest - signature: c1391d813f0596e30497d180105f3e2a0defd24f4c5d15d0bdfa22dc905f7e42
//
