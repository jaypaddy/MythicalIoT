# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import os
import asyncio
import uuid
from azure.iot.device.aio import IoTHubModuleClient
from azure.iot.device import Message
from azure.iot.device import MethodRequest
from azure.iot.device import MethodResponse

import time

messages_to_send = 10


async def main():
    # The client object is used to interact with your Azure IoT hub.
    module_client = IoTHubModuleClient.create_from_edge_environment()

    # define behavior for receiving an input message on input1
    async def input1_listener():
        while True:
            input_message = await module_client.receive_message_on_input("input1")  # blocking call
            print("the data in the message received on input1 was ")
            print(input_message.data)
            print("custom properties are")
            print(input_message.custom_properties)

    # define behavior for receiving an method message on method
    async def method1_listener():
        while True:
            methodReq = await module_client.receive_method_request("method1")  # blocking call
            print("the data in the message received on method1 was ")
            print("Request ID:",methodReq.request_id)
            print("Name:",methodReq.name)
            print("Payload:",methodReq.payload)

            methodResponse =  MethodResponse.create_from_method_request(methodReq, 200, None)
            await module_client.send_method_response(methodResponse)

    # Connect the client.
    await module_client.connect()

    async def send_test_message():
        i = 1
        while True:
            print("sending message #" + str(i))
            msg = Message("test wind speed " + str(i))
            msg.message_id = uuid.uuid4()
            msg.correlation_id = "correlation-1234"
            msg.custom_properties["tornado-warning"] = "yes"
            await module_client.send_message(msg)
            print("done sending message #" + str(i))
            time.sleep(5)
            i = i + 1


    # send `messages_to_send` messages in parallel
    await asyncio.gather(send_test_message(),input1_listener(), method1_listener())


    # finally, disconnect
    await module_client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())

    # If using Python 3.6 or below, use the following code instead of asyncio.run(main()):
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main())
    # loop.close()