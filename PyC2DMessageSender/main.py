# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import os
import asyncio
import uuid
import json
import time
from azure.iot.device.aio import IoTHubModuleClient
from azure.iot.device import Message
from azure.iot.device import MethodRequest
from azure.iot.device import MethodResponse



async def main():
    IOT_DEVICE_CONNSTR="HostName=mythicaledge1.azure-devices.net;DeviceId=macbook;SharedAccessKey=8BcwaCRkstEkyFBwwV5zTpWnLkro0uUWGR2tSrjW3kg="

    module_client = IoTHubModuleClient.create_from_connection_string(IOT_DEVICE_CONNSTR)

    method_name = "method1"
    named_tuple = time.localtime() # get struct_time
    time_string = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)
    payload = json.dumps(dict({'msg': 'Welcome to Digital Display', 'DtTm:' : time_string }))


    method_params = dict({'method_name': method_name, 'payload': time_string, 'connect_timeout_in_seconds': 10})
    methodResponse = await module_client.invoke_method(method_params, 'macbook', 'PySendModule')
    print("ResponseId:",methodResponse.status)
    print("Payload:",methodResponse.payload)

    module_client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())