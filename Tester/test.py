# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import os
import asyncio
import uuid

import time

messages_to_send = 10
message_to_display="Hello"

async def main():
    # The client object is used to interact with your Azure IoT hub.

    # define behavior for receiving an input message on input1
    async def input1_listener():
        while True:
            global message_to_display
            print("input1_listener" , message_to_display)
            await asyncio.sleep(1)

            

    # define behavior for receiving an method message on method
    async def method1_listener():
        while True:
            global message_to_display
            print("method1_listener" , message_to_display)
            await asyncio.sleep(1)



    async def send_test_message():
        i = 1
        while True:
            global message_to_display
            message_to_display = "sending message #" + str(i)
            print(message_to_display)
            await asyncio.sleep(1)
            i = i + 1

    # send `messages_to_send` messages in parallel
    #send_test_message(),input1_listener(), 
    await asyncio.gather(method1_listener(), send_test_message())



if __name__ == "__main__":
    asyncio.run(main())

