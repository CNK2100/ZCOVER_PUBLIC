# -*- coding: utf-8 -*-
import sys
import os
import time
from util.PacketMutator import *

from collections import OrderedDict

import pandas as pd # sudo apt-get install python-pandas 
import xml.etree.ElementTree as ET

try:
    from rflib import *
except ImportError:
    print("\n  [!] Error : Please install rflib... Program exiting...\n")
    sys.exit(1)

XMLPath = './ZWave_custom_cmd_classes.xml'

WFLPath = "./wfl/"
CSVPath = "./csv/"

makeRepo = [WFLPath, CSVPath]
for eachRepo in makeRepo:
    if not os.path.exists(eachRepo):
        os.makedirs(eachRepo)

d1 = None
d2 = None 
frequency = None
homeID = None
nodeID = None


def setting():
    try:
        ## Frequency setting
        frequency = frequency_setting()

        ## Dongles Configuration
        radioDongleConfig(frequency)

    except KeyboardInterrupt:
        print("\n  [!] User interruption at start! Exiting ...!")
        print("\n  [!] Please RESET Radio Dongle \n")
        return
    
    except ChipconUsbTimeoutException:
        pass


def frequency_setting():
    print("\n ---------------------[Z-Wave Frequency Selection]---------------------")
    print("\n  [*] Please select the Z-Wave Frequency from the list below : [1 to 3] ")
    print("\n  [*] Type [1] for USA (908 MHz) [2] Korea (920 MHz) [3] EU (868 MHz)")

    try:
        freq_typed = eval(raw_input("\n\t [+] Select your device frequency (i.e. 1 ,2, or 3) : "))

        if freq_typed == 1:
            frequency = 908420000 ## old devices
            # frequency = 916000000  ## recent devices
        elif freq_typed == 2:
            frequency = 920900000
        elif freq_typed == 3:
            frequency = 868399841
        else:
            print("\n  [!] Invalid Z-Wave frequency! Select from 1 to 3! Exiting...")
            sys.exit(1)

    except Exception as e:
        print("\n  [!] Error found: " + str(e))
        print("\n  [!] Invalid Z-Wave frequency! Select from 1 to 3! Exiting...")
        sys.exit(1)

    return frequency


def radioDongleConfig(frequency):
    global d1, d2
    d1 = RfCat(0, debug = False)
    d2 = None
    zwaveFrequency = frequency

    try:
        ## Configuring Dongle 1
        d1.setFreq(zwaveFrequency)  # US Frequency
        d1.setMdmModulation(MOD_2FSK)
        d1.setMdmSyncWord(0xaa0f)
        d1.setMdmDeviatn(20629.883)
        d1.setMdmChanSpc(199951.172)
        d1.setMdmChanBW(101562.5)
        d1.setMdmDRate(39970.4)
        d1.makePktFLEN(48)
        d1.setEnableMdmManchester(False)
        d1.setMdmSyncMode(SYNCM_CARRIER_15_of_16)
        d1.setModeIDLE()
        return

    except Exception as e:  # work on python 2.x
        print("\n  [!] Connect RF Dongles 1")
        print("\n  [!] Error: " + str(e))
        cleanupDongleFinal(d1)
        cleanupDongleFinal(d2)
        sys.exit(1)


def cleanupDongleFinal(d):
    if d == None:
        pass
    else:
        ## Resetting the First Dongle
        d.setModeIDLE()
        d.cleanup()
        d.RESET()


def target_setting(homeID, nodeID):
        print("\n -------------------------------[Target Setting]-------------------------------")
        homeID = raw_input("\n\t  [+] Please type HomeID: (i.e. C6BD818E)    : ")
        nodeID = raw_input("\n\t  [+] Please type NodeID: (i.e. 0A)    : ")

        return homeID, nodeID


def ExtractUniqueCMD():
    UniqueCMD = []
    
    tree = ET.parse(XMLPath)
    root = tree.getroot()

    for CMDCL in root.findall("cmd_class"):
        for CMD in CMDCL.findall("cmd"):
            CMD_key = CMD.get('key')
            UniqueCMD.append(CMD_key)
        
    UniqueCMD = list(set(UniqueCMD))
    
    return sorted(UniqueCMD)


def ExtractUniquePARAM():
    UniquePARAM = []
    
    tree = ET.parse(XMLPath)
    root = tree.getroot()

    for CMDCL in root.findall("cmd_class"):
        for CMD in CMDCL.findall("cmd"):
            for PARAM in CMD.findall("param"):
                PARAM_key = PARAM.get('key')
                UniquePARAM.append(PARAM_key)
        
    UniquePARAM = list(set(UniquePARAM))
    
    return sorted(UniquePARAM)


def ExtractAllData():
    AllData = {}
    
    tree = ET.parse(XMLPath)
    root = tree.getroot()
    
    for CMDCL in root.findall("cmd_class"):
        CMDCL_key = CMDCL.get('key')
        CMDCL_name = CMDCL.get('name')

        if CMDCL_key not in AllData:
            AllData[CMDCL_key] = {}
        
        for CMD in CMDCL.findall("cmd"):
            CMD_key = CMD.get('key')

            if CMD_key not in AllData[CMDCL_key]:
                AllData[CMDCL_key][CMD_key] = []
            
            for PARAM in CMD.findall("param"):
                PARAM_key = PARAM.get('key')

                AllData[CMDCL_key][CMD_key].append(PARAM_key)

                AllData[CMDCL_key][CMD_key] = list(set(AllData[CMDCL_key][CMD_key]))

    return AllData


def main():
    global d1, d2
    global homeID, nodeID

    setting()

    if d1 == None:
        return
    

    ### Known properties fingerprinting
    argc = len(sys.argv)
    for i in range(argc):
        s = sys.argv[i]
        if i < argc:
            ## Target Setting
            homeID, nodeID = target_setting(homeID, nodeID)


    homeID = homeID.decode("hex")
    nodeID = nodeID.decode("hex")


    ListedCMDCL = [
        "0x5E","0x22","0x85","0x70","0x56","0x7A","0x72","0x73","0x8A","0x55",
        "0x86","0x59","0x5A","0x6C","0x74","0x98","0x9F"
    ] 

    HiddenCMDCL = [
        "0x7B", "0xA2", "0xA1", "0xA0", "0x20", "0x21", "0x63", "0x84", "0x87", "0x80", 
        "0x81", "0x82", "0x88", "0x89", "0xF100", "0x8C", "0x78", "0x71", "0x75", "0x77", 
        "0x76", "0x6F", "0x6B", "0xEF", "0x91", "0x90", "0x01", "0x02"
    ]

  
    AllCtrlCMDCL = []
    AllCtrlCMDCL.extend(HiddenCMDCL) 
    AllCtrlCMDCL.extend(ListedCMDCL)

    UniqueCMD = ExtractUniqueCMD() 
    UniquePARAM = ExtractUniquePARAM()
    AllData = ExtractAllData() 

    ## Prioritize CMDCL
    SortedCMDCL = {}
    for EachCMDCL in AllCtrlCMDCL:
        try: 
            SortedCMDCL[EachCMDCL] = len(AllData[EachCMDCL])
        except KeyError:
            SortedCMDCL[EachCMDCL] = 0

    FinalAllCtrlCMDCL = sorted(SortedCMDCL.items(), key=lambda item: item[1], reverse=True)
    FinalAllCtrlCMDCL = OrderedDict(FinalAllCtrlCMDCL)

    Mutator(d1, homeID, nodeID, UniqueCMD, UniquePARAM, AllData, list(FinalAllCtrlCMDCL.keys())) 


if __name__ == "__main__":
    main()
