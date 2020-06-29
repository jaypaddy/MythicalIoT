import logging

import azure.functions as func
import time
import urllib
import hmac
import hashlib
import base64
import os
import requests
import json

def get_auth_token(iothubName, sas_name, sas_value):
    """
    Returns an authorization token dictionary 
    for making calls to Event Hubs REST API.
    """
    #https://<iothubName>.azure-devices.net/twins/<deviceId>/modules/<moduleName>/methods?api-version=2020-03-13

    uri = urllib.parse.quote_plus("{}.azure-devices.net" \
                    .format(iothubName))
    logging.info(uri)
    sas = sas_value.encode('utf-8')
    expiry = str(int(time.time() + 10000))
    string_to_sign = (uri + '\n' + expiry).encode('utf-8')
    signed_hmac_sha256 = hmac.HMAC(sas, string_to_sign, hashlib.sha256)
    signature = urllib.parse.quote(base64.b64encode(signed_hmac_sha256.digest()))
    return  {
             "uri" : uri,
             "token":'SharedAccessSignature sr={}&sig={}&se={}&skn={}' \
                     .format(uri, signature, expiry, sas_name)
            }


#Need a way to refresh it after long cool down
#sas_string = get_auth_token(os.getenv('IOTHUBNAME'),\
#                    os.getenv('DEVICEID'),\
#                    os.getenv('MODULENAME'),\
#                    os.getenv('APIVERSION'), \
#                    os.getenv('SAS_NAME'),\
#                    os.getenv('SAS_VALUE'))

def sendDisplayMessage(msg):
    #Make a HTTPS CALL using SAS
    #sas_string = get_auth_token(os.getenv('IOTHUBNAME'), \
    #                            os.getenv('SAS_NAME'), \
    #                            os.getenv('SAS_VALUE'))

    sas_string=dict({"token":os.getenv("SAS_TOKEN")})
    headers = {'Content-type': 'application/json',
                'Authorization': sas_string["token"]
                }
    named_tuple = time.localtime() # get struct_time
    time_string = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)
    message_json = json.dumps(dict({'msg': msg, 'dttm:' : time_string }))
    payload_json = json.dumps(dict({
                "methodName": os.getenv('METHODNAME'),
                "respetthodonseTimeoutInSeconds": os.getenv('TIMEOUT_SECS'),
                "payload": message_json
            }))
    url = "https://{}.azure-devices.net/twins/{}/modules/{}/methods?api-version={}" \
                    .format(os.getenv('IOTHUBNAME'), \
                    os.getenv('DEVICEID'), \
                    os.getenv('MODULENAME'), \
                    os.getenv('APIVERSION') )
    r = requests.post( url, data=payload_json, headers=headers, verify=False)
    logging.info(r.content)

    return r.content


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    msg = req.params.get('msg')
    if not msg:
        try:
            req_body = req.get_json()
        except ValueError:
            msg = 'Welcome to Intelligent Edge'
        else:
            name = req_body.get('msg')


    if msg:
        response = sendDisplayMessage(msg)
        return func.HttpResponse(response)
    else:
        return func.HttpResponse(
             "Please pass a message on the query string or in the request body",
             status_code=400
        )
