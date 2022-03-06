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

    #sus detect
    if ("7 10 7"in visemeStream) or ("7 13 7" in visemeStream):
        if random.randint(0, 100)> 50:
            print("just stop")
        else:
            print("why did you say that")
        client.send_message("/avatar/parameters/Collar", True)
        time.sleep(1)
        client.send_message("/avatar/parameters/Collar",False)
        visemestore.clear()

    return
###########################################################



def StarServer():
    dispatcher.map("/avatar/parameters/Viseme", visemeHandler, "viseme")
    dispatcher.map("/avatar/parameters/MuteSelf", muteHander, "Muted")
    dispatcher.map("/avatar/parameters/HeartBeat", heartHander, "HeartBeat")

    server = osc_server.ThreadingOSCUDPServer((VRCHostIP, oscVRCServerPort), dispatcher)
    print("Serving on {}".format(server.server_address))
    server.serve_forever()


    return
def StartClient():
    while True:

        #BPM
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
