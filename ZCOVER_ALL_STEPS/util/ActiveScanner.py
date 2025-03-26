import sys
import time

try:
    from rflib import *
except ImportError:
    print("\n  [!] Error : Please install rflib... Program exiting...\n")
    sys.exit(1)


def ActiveScan(d1, homeID, nodeID):
    NIF, NIF_len = ActiveScanNIF(d1, homeID, nodeID)
    if (NIF != None) and (NIF_len != None):
        print("\n\t  [+] Sniff NIF Pkt : " + NIF)
        ListedCMDCL = ExtractListedCMDCL(NIF, (NIF_len * 2))
    else:
        print("\n\t  [!] Sniff NIF Packet is None... Please run it again !")
        exit(1)

    return ListedCMDCL


def ActiveScanNIF(d1, homeID, nodeID):
    deviceAck = None
    NIF = None
    NIF_len = None

    print("\n ----------------------------[Active Scanning]----------------------------")

    Req_NIF = generate_packet(homeID, nodeID, "\x01\x02") # Request NIF

    t1 = time.time()

    while time.time() - t1 < 5:
        try:
            d1.RFxmit(invert(Req_NIF))
            d1.setModeRX()
            deviceAck = d1.RFrecv(40)[0]
            deviceAck = invert(deviceAck)

            if deviceAck:
                NIF_len = int(deviceAck.encode("hex")[14:16], base=16)
                deviceAck = deviceAck[0:NIF_len]
                deviceAck = deviceAck.encode("hex")

                if deviceAck[0:8] == homeID.encode("hex") and deviceAck[18:20] == "01" and deviceAck[20:22] == "01":
                    NIF = deviceAck
                    break
        
        except ChipconUsbTimeoutException:
            pass

        except KeyboardInterrupt:
            d1.setModeIDLE()
            print("\n  [!] CTRL + C Pressed!! Exiting...!")
            return

        except RuntimeWarning:
            print("\n  [!] Warning")

    return NIF, NIF_len


def generate_packet(homeID, nodeID, payload):
    header = "\x11\x01"
    # header = "\x41\x01"
    src = "\xC8"

    d_len = len(homeID) + len(src) + len(header) + len(nodeID) + len(payload) + 2 # 2 = len(1 byte) + cs(1 byte)
    d_len = format(d_len, '02x')
    d_len = d_len.decode("hex")

    init = "\x00\x0E" 
    cs = checksum(init + homeID + src + header + d_len + nodeID + payload)

    packet = homeID + src + header + d_len + nodeID + payload + cs

    return packet


def checksum(data):
    b = 255
    for i in range(2, len(data)):
        b ^= int(data[i].encode("hex"), 16) # ^ is XOR operator
    return format(b, '02x').decode("hex")


def invert(data):
    datapost = ''
    for i in range(len(data)):
        datapost += chr(ord(data[i]) ^ 0xFF)
    return datapost


def ExtractListedCMDCL(NIF, NIF_len):
    ## ListedCMDCL(= Supported CMDCL)
    ListedCMDCL = []

    for i in range(34, NIF_len-2, 2):
        cmd_class_key = NIF[i:i+2]
        ListedCMDCL.append("0x"+cmd_class_key.upper())

    return ListedCMDCL
