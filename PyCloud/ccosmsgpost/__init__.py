import logging

import azure.functions as func
import time
import urllib
import hmac
import hashlib
import base64
import os

def get_auth_token(iothubName, deviceId, moduleName,version, sas_name, sas_value):
    """
    Returns an authorization token dictionary 
    for making calls to Event Hubs REST API.
    """
    #https://<iothubName>.azure-devices.net/twins/<deviceId>/modules/<moduleName>/methods?api-version=2018-06

    uri = urllib.parse.quote_plus("https://{}.azure-devices.net/{}/modules/{}/methods?api-version={}" \
                    .format(iothubName,deviceId,moduleName,version ))
    sas = sas_value.encode('utf-8')
    expiry = str(int(time.time() + 10000))
    string_to_sign = (uri + '\n' + expiry).encode('utf-8')
    signed_hmac_sha256 = hmac.HMAC(sas, string_to_sign, hashlib.sha256)
    signature = urllib.parse.quote(base64.b64encode(signed_hmac_sha256.digest()))
    return  {
             "token":'SharedAccessSignature sr={}&sig={}&se={}&skn={}' \
                     .format(uri, signature, expiry, sas_name)
            }

#Need a way to refresh it after long cool down
sas_string = get_auth_token(os.getenv('IOTHUBNAME'),\
                    os.getenv('DEVICEID'),\
                    os.getenv('MODULENAME'),\
                    os.getenv('APIVERSION'), \
                    os.getenv('SAS_NAME'),\
                    os.getenv('SAS_VALUE'))

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    
    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello {name}!")
    else:
        return func.HttpResponse(
             "Please pass a name on the query string or in the request body",
             status_code=400
        )
