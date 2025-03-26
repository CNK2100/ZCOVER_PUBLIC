from collections import defaultdict
import sys
import time

try:
    from rflib import *
except ImportError:
    print("\n  [!] Error : Please install rflib... Program exiting...\n")
    sys.exit(1)


def PassiveScan(d1, homeID, nodeID):
    homeID = None
    homeID_nodeID_list = defaultdict(list)

    print("\n -------------------------------[Passive Scanning]-------------------------------")
    print("\n  [*] Scanning Z-Wave devices for 30 seconds! ")
    print("\n  [*] Please create traffic by turning on and off your Z-Wave devices")
    time.sleep(0.025)

    t1 = time.time()

    while time.time() - t1 < 30: # Test for 30 seconds
        try:
            d1.setModeRX()
            deviceAck = d1.RFrecv(10)[0]
            d1.setModeIDLE()
            deviceAck = invert(deviceAck)

            ## Testing Device Status
            if deviceAck:
                deviceAck = deviceAck[0:10]
                deviceAck = deviceAck.encode("hex")

                ## Decode Z-wave Frame
                homeID = deviceAck[0:8]
                nodeID = deviceAck[8:10]

                if homeID not in homeID_nodeID_list.keys():
                    print("\n\t [++] New Z-Wave homeID & nodeID found :    " + str(homeID) + "    " + str(nodeID))
                    homeID_nodeID_list[homeID].append(nodeID)

                if homeID in homeID_nodeID_list.keys():
                    if nodeID not in homeID_nodeID_list[homeID]:
                        print("\n\t [++] New Z-Wave homeID & nodeID found :    " + str(homeID) + "    " + str(nodeID))
                        homeID_nodeID_list[homeID].append(nodeID)

        
        except ChipconUsbTimeoutException:
            pass

        except KeyboardInterrupt:
            d1.setModeIDLE()
            print("\n  [!] CTRL + C Pressed!! Exiting...!")
            return
        
        except RuntimeWarning:
            print("\n  [!] Warning")

        except Exception as e:
            d1.setModeIDLE()
            print ("\n  [!] Thread Wait!\n")
            print(e)


    if homeID == None:
        print("\n  [!] No Z-Wave Network found! Turn on/Off your devices during Scanning!")
        exit(1)
    else:
        PassiveScanSummary(homeID, homeID_nodeID_list)

    return homeID, nodeID


def invert(data):
    datapost = ''
    for i in range(len(data)):
        datapost += chr(ord(data[i]) ^ 0xFF)
    return datapost


def PassiveScanSummary(homeID, homeID_nodeID_list):
    print("\n ---------------------------[Passive Scanning Summary]---------------------------")

    for homeID in homeID_nodeID_list.keys():
        print("\n\t homeID  :  " + str(homeID))
        print("\n\t nodeID  :  " + str(homeID_nodeID_list[homeID]))
        print