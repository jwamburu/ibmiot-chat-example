# -*- coding: utf-8 -*-
# 
# author: john mbari wamburu | jwamburu@ke.ibm.com
#

import time
import json

import ibmiotf.device
import ibmiotf.application


organization = ""


# Device Settings
device_id = "JohnWamburu"
device_type = "ChatDevice"
device_auth_token = ""


# Event settings
event_type = "chat"
msg_format = "json"


# Application Settings
application_id = "ApplicationForJohnWamburu"
application_auth_key = ""
application_auth_token = ""



# Client Implementation Starts Here
try:
    options = {
        "org": organization,
        "type": device_type,
        "id": device_id,
        "auth-method": "token",
        "auth-token": device_auth_token
    }
    client = ibmiotf.device.Client(options)
except ibmiotf.ConnectionException  as e:
    print("Client was unable to connect to IBM IoT : {}".format(e))

client.connect()



# Application Implementation Starts Here
try:
    options = {
        "org": organization,
        "id": application_id,
        "auth-method": "apikey",
        "auth-key": application_auth_key,
        "auth-token": application_auth_token
    }
    application = ibmiotf.application.Client(options)
except ibmiotf.ConnectionException  as e:
    print("Application was unable to connect to IBM IoT : {}".format(e))


def chat_events_callback(event):
    """
    What to do with messages received from device
    """
    data = json.loads(event.data)
    print("{} : {}".format(event.deviceId, data.get("d").get("message")))
    
    
application.connect()
application.deviceEventCallback = chat_events_callback
application.subscribeToDeviceEvents(
    deviceType = device_type,
    deviceId = "JohnMbari",
    event = event_type,
    msgFormat = msg_format
)


def start_chat():
    """
    Get user input and send to subscribed applications. Quit on 'q'
    """
    print("Enter a message to start chatting! \n")
    message = None
    while message != "q":
        message = input()
        data = {
            "d": {
                "message" : message
            }
        }
        client.publishEvent(event_type, msg_format, json.dumps(data))


if __name__ == "__main__":
    start_chat()
