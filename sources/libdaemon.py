#!/usr/bin/python3
# -*-coding:UTF8 -*

import os
import signal

from time import strftime

try:
    from scapy.all import IP, UDP, DNS, sr1, DNSQR
except ImportError as err:
    print(err)
    print("""
Scapy for python3 does not seem to be installed.
If you are on a Debian system, please use apt-get, \
aptitude, synaptic or any package manager to install "python3-scapy".
With apt-get or aptitude, use the following commands:
#> apt-get install python3-scapy
#> aptitude install python3-scapy
If you have pip3, install python3-scapy with the following command :
$> pip3 install scapy-python3.""")


class Killer:
    """Traps SIGINT and SIGTERM signals.

    This allows you to quit the daemon properly."""
    kill_now = False

    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, signum, frame):
        self.kill_now = True



def log(logFile, level, text):
    """Format a log line and write it in the file passed as argument.

    args   :
        logFile : str : path of the log file
        level   : int : log level ( 0->INFO, 1->WARNING, 2->FATAL )
        text    : str : text to be written in the log file
    return : None"""
    loglevel = {0 : " : \x1b[32;1mINFO\x1b[0m : ",
        1 : " : \x1b[33;1mWARNING\x1b[0m : ",
        2 : " : \x1b[31;1mFATAL\x1b[0m : "}
    msg = strftime("%d/%m/%Y %T") + loglevel[level] + text + "\n"
    with open(logFile, "a") as file:
        file.write(msg)


def getPublicIP():
    """Ask OpenDNS for our public IP address.

    args   : None
    return : str : our own public IP address"""
    dnsip = '208.67.222.222'
    sitewww = 'myip.opendns.com'
    dnsquery = IP(dst=dnsip) / UDP(dport=53) / DNS(rd=1, qd=DNSQR(qname=sitewww, qtype="A"))
    return sr1(dnsquery, verbose=0)['DNS'].an.rdata


def daemonize(pidFile, logFile):
    """Allows the server to become a daemon using the fork() sys call.

    args   :
        pidFile : str : path of the log file
        logFile : str : path of the pid file
    return : None"""
    fpid = os.fork()
    if fpid != 0:
        pid = str(fpid)
        log(logFile, 0, "Starting server with PID \x1b[35;1m{0}\x1b[0m !".format(pid))
        with open(pidFile, 'w') as file:
            file.write(pid)
        os.sys.exit(0)


def exiting(logFile, paste_url, api):
    """This allows you to quit the daemon properly.

    args    :
        logFile   : str : path of the log file
        paste_url : str : url of the last pastebin paste
        api       : instance of Api from sources.pastebinAPI module
    return : None"""
    api.delete(paste_url.split(sep="/")[-1])
    log(logFile, 0, "Exiting, old paste deleted.")
