# ZCOVER PUBLIC DEV

## Summary

ZCOVER is an approach for uncovering Z-Wave controller vulnerabilities through systematic security analysis of application layer implementation.
ZCOVER found flaws in  major Z-Wave controllers. These vulnerabilities allow an attacker to inject malicious Z-Wave packets that can manipulate controllers' internal memory and functionality causing a denial-of-service (DoS) on smart home system. A DoS on the Z-Wave controller can disable intrusion and event notifications to the remote house owner resulting in illegal house access without the security systems being activated.

ZCOVER-Public is distributed in the hope that it will be useful to researchers, but WITHOUT ANY WARRANTY; hence, be responsible while using ZCOVER-Public.

We recommend testing ONLY your PERSONAL DEVICES in a CLOSED CONTROLLED environment to avoid jamming 908 MHz or ANY frequency that is used for different purpose per COUNTRY. It may be ILLEGAL to send packets in reserved frequencies without a prior POLICE or Government AUTHORIZATION.


## For the academic/public use, the researcher MUST cite the following paper:

1. C.K. Nkuba, J. Kang, S. Woo, and H. Lee, "ZCOVER: Uncovering Z-Wave Controller Vulnerabilities Through Systematic Security Analysis of Application Layer Implementation", The 55th Annual IEEE/IFIP International Conference on Dependable Systems and Networks (DSN 2025), 2025.

## Source Code and libraries requirement
Additional README file is available in ZCOVER_ALL_STEPS folder describing the source code details and library requirement.

## Vulnerability description

Denial of Service (DoS) vulnerabilities in Z-Wave chipsets. These vulnerabilities may allow a remote, unauthenticated attacker to inject malicious packets to the Z-Wave controller to cause DoS.

#### CVSS Severity: High

## Discoverer

Thanks to Dr. Carlos Kayembe Nkuba, Jimin Kang, Professor Seunghoon Woo, and Professor Heejo Lee from Korea University for reporting these vulnerabilities.

## Responsible disclosure

We filed several vulnerability reports to the US CERT/CC division and US. MITRE in order to work with the  respective chipsets and device manufacturers to fix and mitigate the threats that we discovered.

12 CVES were assigned by US. MITRE and SiLabs: CVE-2024-50931, CVE-2024-50930,  CVE-2024-50929, CVE-2024-50928, CVE-2024-50924, CVE-2024-50921, CVE-2024-50920,  CVE-2023-6643, CVE-2023-6642, CVE-2023-6641, CVE-2023-6640, and  CVE-2023-6533.

Moreover, two security advisories were assigned by Silicon Labs (SiLabs) :  "Security Advisory A-00000502 and Security Advisory A-00000505".

### Vendor contact timeline

2023-11-12: Contacting US. CERT/CC

2023-11-13: CERT/CC added 17 vendors to the case

2023-12-08: SiLabs assigned 5 CVEs.

2024-02-15: Silicon Labs (SiLabs) published a Security Advisory A-00000502

It can be accessible after creating a free account at: https://community.silabs.com/s/alert/a45Vm00000000knIAA/a00000502

2024-02-29 : Silicon Labs (SiLabs) published a second Security Advisory A-00000505

It can be accessible after creating a free account at: https://community.silabs.com/s/contentdocument/069Vm000002020u

2024-12-10: US. MITRE published 7 CVEs


### Affected Device Manufacturers and Service Providers

All Z-Wave device manufacturers and members of the Z-Wave Alliance (e.g., ADT Inc, Aeotec, Amazon, Dome Home Automation, Fibaro, Google, Jasco, Linear, Philips Electronics, Philips Healthcare, Samsung SmartThings, Schlage, Yale, Silicon Labs, Smartthings, LG, Zooz, etc.)



### Additional Information

With the use of tools and transceivers that can decode Z-Wave frame( e.g., Scapy-radio with HackRF One; Yard Stick One; RFCat ; RTL-SDR; Zniffer with Sigma UZB) an attacker sniffs and captures any Z-Wave communication of a target Z-Wave smart home. 
Then he retrieves the Z-Wave HomeID and NodeID of devices that are transmiting packets in the network. 
With the knowledge of the HomeID, the attacker can brute force the Z-Wave network to know all remaining available smart devices in the network. This is achieved by sending to all possible Z-Wave node (2 to 232) 
either these Z-Wave frames: No Operation (NOP), SWITCH_BINARY_GET, or Node Information (NIF), SECURITY_NONCE_GET, SECURITY_2_NONCE_GET  to get the acknowledgement (ACK) from devices. 

From this ACK the attacker retrieves the node ID of devices that responded and their capabilities. 

With the knowledge of the Z-Wave HomeID and NodeID of the device, the attacker crafts a malicious packet with a desired malicious payload and sends it to the target Z-Wave device by using a customized Z-Wave packet management software and hardware such as  HackRF One,  Yard Stick One,  RFCat, or CC1110. 

The controller will accept and validate the malicious packet, which cause a DoS. These attacks are critical because they render the Z-Wave controller vulnerable to DoS attacks, which make their service inaccessible to authentic smart home users. 

### How does an attacker exploit this vulnerability?

Attacker and target device need to be within a range of 40 to 100 meters. 
The range can be increased by using an advanced Software-Defined Radio (SDR) hardware.

### What is the impact of this vulnerability?

Denial of service (DoS) on Z-Wave controller.


### Attack Vectors

By crafting a malicious Z-Wave packet and sending it to the Z-Wave controller and devices. 

### Attack Type

Proximate remote attack

### Impact Denial of Service

Denial of Service on the controller.


## Vendor of Product

Silicon Labs ( SiLabs) Z-Wave chipset, which is  present in ALL Z-Wave controller from all the manufacturers worlwide. All members of the Z-Wave Alliance are affected (e.g., ADT Inc, Aeotec, Amazon, Dome Home Automation, Fibaro, Google, Jasco, Linear, Philips Electronics, Philips Healthcare, Samsung SmartThings, Schlage, Yale, Silicon Labs, Smartthings, LG, Zooz, etc.)


### Affected Product Code Base

Z Wave controllers with Silicon Labs Chipset


## Fix/Workaround Method

Check SiLabs Security Advisory A-00000502

It can be accessible after creating a free account at: https://community.silabs.com/s/alert/a45Vm00000000knIAA/a00000502

Check SiLabs Security Advisory A-00000505

It can be accessible after creating a free account at: https://community.silabs.com/s/contentdocument/069Vm000002020u

## Reference

- https://ccs.korea.ac.kr/pds/Vulnerabilities_in_ZWave.html
- https://github.com/CNK2100/2024-CVE/blob/main/README.md
- Create a free account at https://community.silabs.com to access the response document from the affected vendor, Silicon Labs (SiLabs).
- https://community.silabs.com/068Vm00000211lw
- https://community.silabs.com/s/contentdocument/069Vm000001Gv50
- Experiment videos can be accessed at below two links:
- https://drive.google.com/file/d/1LBycOFbQThFxuGedefVfNqNa0TbTE0R0/view
- https://drive.google.com/file/d/1aZMcGRUVtweYkWlcHzWRsl1jhp1nSBYs/view

## Ethical considerations

The ZCOVER public version WILL provide source code for core Z-Wave fuzzing functionalities while reducing advanced features and PoC Attacks that could be misused by bad actors to attack smart home devices. For the same ethical considerations, we are not releasing the ZCOVER PoC exploit code.

## About

This repository is maintained by K. Jimin and Dr. N. Carlos. For reporting bugs, you can submit an issue to the GitHub repository.
