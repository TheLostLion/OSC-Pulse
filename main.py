###########################################################
# VRC OSC - Lost Lion
###########################################################
import random
import time
import threading
import asyncio
import websocket

try:
    import thread
except ImportError:
    import _thread as thread

from pythonosc import udp_client
from pythonosc import dispatcher
from pythonosc import osc_server




# VRC Host Port
###########################################################
###########################################################

VRCHostIP = "127.0.0.1"
oscVRCClientPort = 9000
oscVRCServerPort = 9001

###########################################################


# HypeRate
###########################################################
###########################################################
HRID = 4068
Key = open("C:\\Users\Lost Lion\PycharmProjects\key.txt", "r")
WebSocketKey = (Key.readline())
Key.close()

import time, json

# put your HyperRate ID here

def StartWebsocket():
    global webSocket
    webSocket = websocket.WebSocketApp("wss://app.hyperate.io/socket/websocket?token=" + WebSocketKey,
                                       on_message=on_message,
                                       on_error=on_error,
                                       on_close=on_close,
                                       on_open=on_open)
    webSocket.run_forever()


def on_message(ws, message):
    #print(message)
    jsonPayload = json.loads(message)
    if jsonPayload["event"] == "hr_update":
        BPM = jsonPayload["payload"]["hr"]
        #print("Current BPM: " + str(BPM))
        client.send_message("/avatar/parameters/HeartBeat", (BPM / 200) * 2 - 1)


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    print("Opened websocket connection")
    thread.start_new_thread(sendConnectionPayload, ())


def sendConnectionPayload():
    print("Sending connection payload")
    webSocket.send('{"topic":"hr:' + str(HRID) + '","event":"phx_join","payload": {},"ref": 0}')
    HeartbeatThread = threading.Thread(target=sendHeartbeat)
    HeartbeatThread.start()


def sendHeartbeat():
    while True:
        print("Sending heartbeat")
        webSocket.send('{"topic": "phoenix","event": "heartbeat","payload": {},"ref": 0}')
        time.sleep(30)


###########################################################



# viseme config
###########################################################
###########################################################
visemestore = []

def muteHander(unused_addr, args, Muted):

    print("mute")
    visemestore.clear()

    return

def visemeHandler(unused_addr, args, viseme):
    visemestore.append (viseme)
    if len(visemestore) >10:
        visemestore.pop(0)
    visemeStream = ""
    for item in visemestore:
        visemeStream += str(item) + " "

    #for testing of viseims
    print(visemestore)

    #collar detect
    # will activate the collar when you say submissive for 1 sec
    # just for testing
    if ("7 12 1 12 7"in visemeStream) or ("7 12 7 12 0" in visemeStream):
        if random.randint(0, 100)> 50:
            print("just stop")
        else:
            print("why did you say that")
        client.send_message("/avatar/parameters/Collar", True)
        time.sleep(1)
        client.send_message("/avatar/parameters/Collar",False)
        visemestore.clear()

    # HeartBeat detect
    # will activate the HeartBeat  for 15 sec
    if ("1 13 8 7" in visemeStream) or ("14 13 7 0" in visemeStream):
        if random.randint(0, 100) > 50:
            print("HeartBeat")
        else:
            print("HeartBeat ooo")
        client.send_message("/avatar/parameters/HeartBeatShow", True)
        time.sleep(15)
        client.send_message("/avatar/parameters/HeartBeatShow", False)
        visemestore.clear()

        # Blue detect
        # will activate the Blue for 20 sec
    if ("8 13 14 0" in visemeStream) or ("8 13 14 13" in visemeStream):
        if random.randint(0, 100) > 50:
            print("wow blue really ")
        else:
            print("green is better")
        client.send_message("/avatar/parameters/Blue", True)
        time.sleep(5)
        client.send_message("/avatar/parameters/Blue", False)
        visemestore.clear()
    return
###########################################################



def StarServer():
    dispatcher.map("/avatar/parameters/Viseme", visemeHandler, "viseme")
    dispatcher.map("/avatar/parameters/MuteSelf", muteHander, "Muted")

    server = osc_server.ThreadingOSCUDPServer((VRCHostIP, oscVRCServerPort), dispatcher)
    print("Serving on {}".format(server.server_address))
    server.serve_forever()


    return
def StartClient():
    while True:

        BPM = 50
        client.send_message("/avatar/parameters/HeartBeat",(BPM/200) * 2 - 1 )
        time.sleep(0.5)

if __name__ == '__main__':
    print("Python OSC Service Running")

    dispatcher = dispatcher.Dispatcher()
    serverThreading = threading.Thread(target=StarServer)
    serverThreading.start()


    client = udp_client.SimpleUDPClient(VRCHostIP, oscVRCClientPort)
    ClientThread = threading.Thread(target=StartClient)
    ClientThread.start()
