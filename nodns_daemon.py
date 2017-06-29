#!/usr/bin/python3

from os import fork, path, environ, mkdir, getpid
from sys import exit
from time import sleep
from sources.libdaemon import log, getPublicIP
from sources.settings import userKey, devKey, TTS, pasteName
from sources.pastebinAPI import Api

filespath = environ['HOME'] + "/.nodns"
if not path.isdir(filespath) :
    mkdir(filespath)
logfile = filespath + "/log"
pidfile = filespath + "/pid"
urlfile = filespath + "/url"

otag = "\x1b[35;1m"
ctag = "\x1b[0m"

api = Api(devKey, userKey)
PID = str(getpid())
with open(pidfile, "w") as file :
    file.write(PID+"\n")
log(logfile, 0, "Server starting with pid {0}.".format(otag+PID+ctag))
log(logfile, 0, """Obtaining our public IP address for the first time...""")
public_ip_adress_ = getPublicIP()
log(logfile, 0, """Public IP address is : {0}""".format(otag+public_ip_adress_+ctag))
log(logfile, 0, """Sending our public IP address to Pastebin...""")
paste_url = api.paste(public_ip_adress_, pasteName).text
with open(urlfile, 'w') as file :
    file.write(paste_url+"\n")
log(logfile, 0, """paste URL is : {0}""".format(otag+paste_url+ctag))

try :
    while True :
        public_ip_adress = getPublicIP()
        if public_ip_adress_ == public_ip_adress :
            public_ip_adress_ = public_ip_adress
            sleep(TTS*60)
        else :
            log(logfile, 0, """Public IP address has changed...""")
            log(logfile, 0, """New public IP address is : {0}.""".format(otag+public_ip_adress+ctag))
            public_ip_adress_ = public_ip_adress
            log(logfile, 0, """Sending our new public IP address to Pastebin...""")
            paste_url = api.paste(public_ip_adress, pasteName).text
            with open(urlfile, 'w') as file :
                file.write(paste_url+"\n")
            log(logfile, 0, """paste URL is : {0}""".format(otag+paste_url+ctag))
            api.delete(paste_url.split(sep="/")[-1])
            log(logfile, 0, "Old paste deleted.")
finally :
    api.delete(paste_url.split(sep="/")[-1])
    log(logfile, 0, "Exiting, old paste deleted.")
    
    

    


