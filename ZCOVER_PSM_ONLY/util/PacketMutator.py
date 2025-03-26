import sys
import time
import datetime
from datetime import datetime
import random

try:
    from rflib import *
except ImportError:
    print("\n  [!] Error : Please install rflib... Program exiting...\n")
    sys.exit(1)

year = datetime.today().year
month = datetime.today().month
day = datetime.today().day
hour = datetime.today().hour
minute = datetime.today().minute
second = datetime.today().second
microsecond = datetime.today().microsecond
log_time = "{0}_{1}_{2}_{3}-{4}-{5}-{6}".format(year, month, day, hour, minute, second, microsecond)
StartTime = time.time()


def Mutator(d1, homeID, nodeID, UniqueCMD, UniquePARAM, AllData, AllCtrlCMDCL_LIST):
    initialize_csv()
    initialize_wfl(homeID, nodeID)

    txcount = 0
    ercount = 0
    NOP = generate_packet(homeID, nodeID, "\x00")

    print("\n ----------------------------[Packet Mutation]----------------------------\n")
    
    ## Target available
    device_state = None
    crash = None
    device_state, crash = send_nop_sniff_ack(d1, homeID, nodeID, NOP)
    if device_state is False:
        ## Mutation
        t2 = time.time()
        idx = 0
        while True:
            if time.time() - t2 > 86400: ## 86400 sec is 24 hour
                break 
            
            AllCtrlCMDCL = AllCtrlCMDCL_LIST[idx]

            idx += 1
            if idx >= len(AllCtrlCMDCL_LIST):
                idx = 0
            
            ## Position-sensitive Mutation
            try: 
                if len(AllData[AllCtrlCMDCL]) == 0:
                    test_time = 3
                else:
                    test_time = len(AllData[AllCtrlCMDCL]) * 3
            except KeyError:
                test_time = 3

            t3 = time.time()
            while time.time() - t3 < test_time:
                try:
                    if len(AllData[AllCtrlCMDCL]) == 0:
                        CMD = random.choice(UniqueCMD) ## unique range random 
                    else:
                        CMD = random.choice(AllData[AllCtrlCMDCL].keys())

                    d1.setModeIDLE()
                    time.sleep(0.5) ## Better for one dongle to avoid Dongle ChipconUSBTimeoutException 

                    if len(AllData[AllCtrlCMDCL]) == 0 or len(AllData[AllCtrlCMDCL][CMD]) == 0:
                        PARAM = random.choice(UniquePARAM) ## unique range random 
                    else:
                        PARAM = random.choice(AllData[AllCtrlCMDCL][CMD])

                except KeyError:
                    CMD = random.choice(UniqueCMD)
                    PARAM = random.choice(UniquePARAM)

                try:  
                    CMDCL = format(int(AllCtrlCMDCL, 16), "02x").decode("hex")
                    CMD = format(int(CMD, 16), "02x").decode("hex")
                    PARAM = format(int(PARAM, 16), "02x").decode("hex")
                    PARAM1 = format(int(random.randint(0, 255)), "02x").decode("hex")
                    PARAM2 = format(int(random.randint(0, 255)), "02x").decode("hex")
                    PARAM3 = format(int(random.randint(0, 255)), "02x").decode("hex")
                    PARAM4 = format(int(random.randint(0, 255)), "02x").decode("hex")
                    PARAM5 = format(int(random.randint(0, 255)), "02x").decode("hex")
                    PARAM6 = format(int(random.randint(0, 255)), "02x").decode("hex")
                    PARAM7 = format(int(random.randint(0, 255)), "02x").decode("hex")
                    PARAM8 = format(int(random.randint(0, 255)), "02x").decode("hex")

                    payload = CMDCL + CMD + PARAM + PARAM1 + PARAM2 + PARAM3 + PARAM4 + PARAM5 + PARAM6 + PARAM7 + PARAM8

                    packet = generate_packet(homeID, nodeID, payload)

                    for _ in range(2):
                        d1.RFxmit(invert(packet))
                        d1.setModeIDLE()
                        time.sleep(0.025)

                    device_state = None
                    crash = None
                    device_state, crash = send_nop_sniff_ack(d1, homeID, nodeID, NOP)
                    if device_state is False:
                        txcount += 1
                        show_console(txcount, packet.encode("hex"))
                        save_csv(homeID, nodeID, txcount, crash, packet.encode("hex"), int(time.time()-StartTime))
                        save_wfl(txcount, crash, packet.encode("hex"))
                    else:
                        ercount += 1
                        txcount += 1
                        save_csv(homeID, nodeID, txcount, crash, packet.encode("hex"), int(time.time()-StartTime))
                        save_wfl(txcount, crash, packet.encode("hex"))
                        print("\n\t\t [!] Device: " + str(nodeID.encode("hex")) + " cannot be reached!")

                except ChipconUsbTimeoutException:
                    pass

                except KeyboardInterrupt:
                    d1.setModeIDLE()
                    print("\n\n\t\t [!] User Interruption during Random Testing! Exiting...")

    else:
        print ("\n\t\t  [!] Device is unavailable !!")
        return

    summary_console(txcount, ercount)
    finish_wfl(txcount, ercount)


def generate_packet(homeID, nodeID, payload):
    # header = "\x11\x01"
    header = "\x41\x01"
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


def send_nop_sniff_ack(d1, homeID, nodeID, NOP):
    deviceAck = None
    crash = "y" # y: crash o / n: crash x
    device_state = True # True: device unavailable / False: device available

    t1 = time.time()
    while time.time() - t1 < 1:
        d1.setModeIDLE()
        time.sleep(0.05)

        try:
            d1.RFxmit(invert(NOP))
            d1.setModeRX()

            deviceAck = d1.RFrecv(11)[0]
            deviceAck = invert(deviceAck)
            
            if deviceAck:
                deviceAck = deviceAck[0:10]
                deviceAck = deviceAck.encode("hex")

                if (deviceAck[0:8] == homeID.encode("hex")) and (
                    deviceAck[8:10] == nodeID.encode("hex")) and (deviceAck[14:16] == "0a"):
                    crash = "n"
                    device_state = False
                    break
            
            elif deviceAck == None:
                print("\n\t\t [!] Device does not respond! Please check it again !")
                device_state = True
                break
        
        except ChipconUsbTimeoutException:
            pass

        except KeyboardInterrupt:
            d1.setModeIDLE()
            print("\n  [!] CTRL + C Pressed!! Exiting...!")
            return

        except RuntimeWarning:
            print("\n  [!] Warning")

    return device_state, crash


def show_console(txcount, pkt):
    sys.stdout.write("\r\x1b[K\t [+] Send pkt: " + str(txcount) + " | Data: " + pkt[0:30] + " ... " + pkt[-2:])
    sys.stdout.flush()


def summary_console(txcount, ercount):
        print("\n\n ------------------------------[SUMMARY]------------------------------")
        print("\n          [*][*][*] Total packets sent        : {0}".format(txcount))
        print("\n          [*][*][*] Total hang(s), error(s)   : {0}".format(ercount))
        print("\n -----------------------------------------------------------------------")


def initialize_wfl(homeID, nodeID):
    wfl_file = open('./wfl/log_{}.wfl'.format(log_time), "a")
    wfl_file.write("{\n")
    wfl_file.write("\t\"toolVer\" : \"{0}\",\n".format("1.0.0"))
    wfl_file.write("\t\"interface\" : \"{0}\",\n".format("Z-Wave"))
    wfl_file.write("\t\"homeId\" : \"{0}\",\n".format(homeID.encode("hex")))
    wfl_file.write("\t\"nodeId\" : \"{0}\",\n".format(nodeID.encode("hex")))
    wfl_file.write("\t\"starting_time\" : \"{0}-{1}-{2} {3}:{4}:{5}.{6}\",\n".format(year, month, day, hour, minute, second, microsecond))
    wfl_file.write("\t\"protocol\" : \"{0}\",\n".format("Z-Wave"))
    wfl_file.write("\t\"packet\" : [\n")
    wfl_file.close()

def save_wfl(txcount, crash, pkt):
    wfl_file = open('./wfl/log_{}.wfl'.format(log_time), "a")
    wfl_file.write("\t\t{")
    wfl_file.write("\"no\" : {0}, ".format(txcount))
    wfl_file.write("\"org_no\" : 1, ")
    if str(crash) == "y":
        wfl_file.write("\"state\" : 3, ")
    else: 
        wfl_file.write("\"state\" : 2, ")
    wfl_file.write("\"crash\" : \"{0}\", ".format(str(crash)))
    wfl_file.write("\"payload\" : {")
    wfl_file.write("\"HID\" : \"0x{0}\", ".format(pkt[0:8]))
    wfl_file.write("\"SRC\" : \"0x{0}\", ".format(pkt[8:10]))
    wfl_file.write("\"FC1\" : \"0x{0}\", ".format(pkt[10:12]))
    wfl_file.write("\"FC2\" : \"0x{0}\", ".format(pkt[12:14]))
    wfl_file.write("\"LEN\" : \"0x{0}\", ".format(pkt[14:16]))
    wfl_file.write("\"DST\" : \"0x{0}\", ".format(pkt[16:18]))
    wfl_file.write("\"CMDCL\" : \"0x{0}\", ".format(pkt[18:20]))
    wfl_file.write("\"CMD\" : \"0x{0}\", ".format(pkt[20:22]))
    wfl_file.write("\"PLD\" : \"0x{0}\", ".format(pkt[22:-2]))
    wfl_file.write("\"CS\" : \"0x{0}\"".format(pkt[-2:]))
    wfl_file.write("}")
    wfl_file.write("},\n")
    wfl_file.close()

def finish_wfl(txcount, ercount):
    wfl_file = open('./wfl/log_{}.wfl'.format(log_time), "a")
    wfl_file.seek(-2, os.SEEK_END)
    wfl_file.truncate()
    wfl_file.write('\n\t]\n')
    wfl_file.write('}')
    wfl_file.close()

    wfl_file = open('./wfl/log_{}.wfl'.format(log_time), "r")
    contents = wfl_file.readlines()
    wfl_file.close()
    contents.insert(7, '\t"count" : {\n\t\t"all" : %d,\n\t\t"crash" : %d,\n\t\t"passed" : %d\n\t},\n' % (
        int(txcount), int(ercount), int(txcount) - int(ercount)))

    wfl_file = open('./wfl/log_{}.wfl'.format(log_time), "w")
    contents = "".join(contents)
    wfl_file.write(contents)
    wfl_file.close()


def initialize_csv():
    csv_file = open('./csv/log_{}.csv'.format(log_time), "a")
    csv_file.write("no,Time,IntTime,homeID,nodeID,crash,packet,HID,SRC,FC1,FC2,LEN,DST,CMDCL,CMD,PARAM,CS\n")
    csv_file.close()

def save_csv(homeID, nodeID, txcount, crash, pkt, time):
    hour = datetime.today().hour
    minute = datetime.today().minute
    second = datetime.today().second

    csv_file = open('./csv/log_{}.csv'.format(log_time), "a")
    csv_file.write(str(txcount)+",")
    csv_file.write("{0}:{1}:{2},".format(hour, minute, second))
    csv_file.write(str(time)+",")
    csv_file.write(homeID.encode("hex")+",")
    csv_file.write(nodeID.encode("hex")+",")
    csv_file.write(str(crash)+",")
    csv_file.write(pkt+",")
    csv_file.write(pkt[0:8]+",")
    csv_file.write(pkt[8:10]+",")
    csv_file.write(pkt[10:12]+",")
    csv_file.write(pkt[12:14]+",")
    csv_file.write(pkt[14:16]+",")
    csv_file.write(pkt[16:18]+",")
    csv_file.write(pkt[18:20]+",")
    csv_file.write(pkt[20:22]+",")
    csv_file.write(pkt[22:-2]+",")
    csv_file.write(pkt[-2:]+"\n")
    csv_file.close()