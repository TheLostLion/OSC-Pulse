import random
import time
import threading

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





# HpyeRate
###########################################################
###########################################################

# put your HyperRate ID here
# HypeRateID = ("https://app.hyperate.io/####")




###########################################################



# viseme config
###########################################################
###########################################################
visemestore = []

def muteHander(unused_addr, args, Muted):

    print("mute")

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
    if ("7 12 1 12 7"in visemeStream) or ("7 12 7 12 0" in visemeStream):
        if random.randint(0, 100)> 50:
            print("just stop")
        else:
            print("why did you say that")
        client.send_message("/avatar/parameters/Collar", True)
        time.sleep(1)
        client.send_message("/avatar/parameters/Collar",False)
        visemestore.clear()

    #HeartBeat detect
    # will activate the HeartBeat  for 25 sec
    if ("1 13 8 7"in visemeStream) or ("14 13 7 0" in visemeStream):
        if random.randint(0, 100)> 50:
            print("HeartBeat")
        else:
            print("HeartBeat ooo")
        client.send_message("/avatar/parameters/HeartBeatShow", True)
        time.sleep(25)
        client.send_message("/avatar/parameters/HeartBeatShow",False)
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
