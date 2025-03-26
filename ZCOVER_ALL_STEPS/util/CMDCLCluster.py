import pandas as pd # sudo apt-get install python-pandas 
import xml.etree.ElementTree as ET

SpecPath = './List of defined Z-Wave Command Classes.xlsx'
XMLPath = './ZWave_custom_cmd_classes.xml'

SlaveDeviceList = [
    "SECURITY_PANEL", "SWITCH", "CHIMNEY_FAN",
    "SCENE", "METER", "THERMOSTAT", "IRRGATION", 
    "RATE_TBL", "DOOR_LOCK", "HUMIDITY", "DMX", "BARRIER_OPERATOR", 
    "WINDOW", "SCREEN", "AV", "SENSOR"
]

ManuallyList = [
    "APPLICATION", "ZIP", "NETWORK_MANAGEMENT", "INTEROPERABLE", "SCHEDULE", 
    "SUPERVISION", "ALARM", "TIME", "MULTI", "IP", "TARIFF", "HRV", "DCP", 
    "PREPAYMENT", "ASSOCIATION", "ANTITHEFT", "MAILBOX", "NO_OPERATION"
]


def RemoveSlaveCMDCL(CMDCLData):
    RemoveUniqueCMDCL1 = {}    
    for CMDCL_name, CMDCL_key in CMDCLData.items():
        flag = 0
        for SlaveDevice in SlaveDeviceList:
            if SlaveDevice + "_" in CMDCL_name or "_" + SlaveDevice in CMDCL_name:
                flag = 1

        if flag == 0:
            RemoveUniqueCMDCL1[CMDCL_name] = CMDCL_key
    
    return RemoveUniqueCMDCL1


def RemoveManuallyCMDCL(RemoveSlaveCMDCL):
    RemoveUniqueCMDCL2 = {}    
    for CMDCL_name, CMDCL_key in RemoveSlaveCMDCL.items():
        flag = 0
        for Manually in ManuallyList:
            if Manually + "_" in CMDCL_name or "_" + Manually in CMDCL_name:
                flag = 1

        if flag == 0:
            RemoveUniqueCMDCL2[CMDCL_name] = CMDCL_key    

    return RemoveUniqueCMDCL2


def ClusteringCMDCL(CMDCLData):
    RemoveUniqueCMDCL1 = RemoveSlaveCMDCL(CMDCLData) 
    RemoveUniqueCMDCL2 = RemoveManuallyCMDCL(RemoveUniqueCMDCL1) 
    
    return sorted(RemoveUniqueCMDCL2.values())


def ExtractSpecAllCMDCL():
    Data = pd.ExcelFile(SpecPath).parse("Command Class")
    DataList = Data.values.tolist()

    SpecAllCMDCL = {}
    for CMDCLData in DataList:
        SpecAllCMDCL[CMDCLData[1]] = CMDCLData[4]
    
    return SpecAllCMDCL


def ExtractXMLAllCMDCL():
    XMLAllCMDCL = {}
    
    tree = ET.parse(XMLPath)
    root = tree.getroot()

    for CMDCL in root.findall("cmd_class"):
        CMDCL_key = CMDCL.get('key')
        CMDCL_name = CMDCL.get('name')

        XMLAllCMDCL[CMDCL_name] = CMDCL_key
    XMLAllCMDCL = dict(sorted(XMLAllCMDCL.items(), key=lambda x: x[1])) 
    
    return XMLAllCMDCL


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
    """ Format
    {
        CMDCL: {
            CMD: [PARAM, PARAM]
            CMD: [PARAM, PARAM]
        }
    }
    """
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