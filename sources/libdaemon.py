#!/usr/bin/python3

import os
try :
    from scapy.all import IP, UDP, DNS, sr1, DNSQR
except ImportError as err :
    print(err)
    print("""
Scapy for python3 does not seem to be installed.
If you are on a Debian system, please use apt-get, aptitude, synaptic or any package manager to install "python3-scapy".
With apt-get or aptitude, use the following commands:
#> apt-get install python3-scapy
#> aptitude install python3-scapy
If you have pip3, install python3-scapy with the following command :
$> pip3 install scapy-python3.""")
from time import strftime

def log(logfile, level, text):
    loglevel={0 : " : \x1b[32;1mINFO\x1b[0m : ",
        1 : " : \x1b[32;1mWARNING\x1b[0m : ",
        2 : " : \x1b[32;1mFATAL\x1b[0m : "}
    msg = strftime("%d/%m/%Y %T") + loglevel[level] + text + "\n"
    with open(logfile, "a") as file :
        file.write(msg)

def getPublicIP():
    """Return own public IP adress"""
    dnsip='208.67.222.222'
    sitewww='myip.opendns.com'
    dnsquery = IP(dst=dnsip) / UDP(dport=53) / DNS(rd=1, qd=DNSQR(qname=sitewww, qtype="A" ))
    return sr1(dnsquery, verbose=0)['DNS'].an.rdata
