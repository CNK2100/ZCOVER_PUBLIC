# ZCOVER ALL STEPS
This is the simplified and reduced version of ZCOVER. It aims to provide to
researchers core information about fuzzing Z-Wave controller devices.

ZCOVER-Public  is distributed in the hope that it will be useful to researchers, 
but WITHOUT ANY WARRANTY; hence, be responsible while using ZCOVER-Public.

We recommend testing ONLY your PERSONAL DEVICES in a CLOSED CONTROLLED environment to avoid jamming 908 MHz or ANY frequency that is used for different purpose per COUNTRY. It may be ILLEGAL to send packets in reserved frequencies without a prior POLICE or Government AUTHORIZATION.

Fuzzing throughput has been reduced as the version runs on ONE YardStick One 
dongle for afordability.

## Supported dongles:
>Hardware:

ZCOVER-Public runs on YardStick One (https://greatscottgadgets.com/yardstickone/)
or Any sub-gigahertz dongle supporting RFCat library.

## Requirements: Python 2.7 due to RFCAT library

### ON UBUNTU 18
```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install python  ## For Python 2
sudo apt-get install libusb-1.0-0-dev
sudo apt-get install python-pip
sudo apt install python-usb libusb-1.0.0 make
sudo apt install python-pydot python-pydot-ng graphviz
sudo apt-get install ipython
sudo apt-get install git
sudo pip install PySide2
sudo apt-get install python-pandas
sudo apt-get install python-numpy
pip install numpy
pip install bitstring
pip install psutil
pip install requests
sudo apt install sdcc
```
### ON UBUNTU 20

```
sudo apt install python2  ## Ubuntu 20
sudo python2 get-pip.py  ## Ubuntu 20
pip2 install requests numpy bitstring psutil pandas iphyton pyside2
pip2 install graphviz pydot ng libusb setuptools wheel

```
## Installation 
>Install RFCAT at https://github.com/atlas0fd00m/rfcat



## Run ZCOVER:

ZCOVER has two options.


### 1. "--p" option
If you don't know the homeID and nodeID of the controller, use this option for passive scanning. 
Create traffic in your Z-Wave network so that ZCover can sniff key properties.

```
python ./Main.py --p
```


### 2. "--s" option
If you know both the homeID and nodeID, use this option for active scanning.

```
python ./Main.py --s
```


## Stop ZCOVER
Fuzzing time can be set manually depending on use case and  here we set it to 24 hours.

```
CTRL + Z
```

## Verifing and retransmitting logged packets or custom packets.

You can  test a log packet generated during fuzz testing or create your own.

* "Packet" can be copied from the  csv/log*** file.
```
usage: python ./PacketTester.py [# of transmission] [Packet]

python ./PacketTester.py 3 1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c
```
