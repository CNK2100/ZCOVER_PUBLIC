# -*- coding: utf-8 -*-
import sys
import time

try:
    from rflib import *
except ImportError:
    print("\n  [!] Error : Please install rflib... Program exiting...\n")
    sys.exit(1)


d1 = None
d2 = None 
frequency = None


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


def invert(data):
    datapost = ''
    for i in range(len(data)):
        datapost += chr(ord(data[i]) ^ 0xFF)
    return datapost


def main():
    global d1, d2

    argc = len(sys.argv)
    if argc != 3:
        print("\t usage: TestPacket.py [Packet Send Count] [Packet]")
        print("\t example: TestPacket.py 3 1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c")
        return
    
    count = sys.argv[1]
    packet = sys.argv[2]

    setting()

    if d1 == None:
        return

    print("\n ---------------------[Testing]---------------------\n")
    for _ in range(int(count)):
        print(packet)
        d1.RFxmit(invert(packet.decode("hex")))
        time.sleep(0.25)


if __name__ == "__main__":
    main()