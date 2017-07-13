#!/usr/bin/python3

import os
from sys import exit
from time import sleep
from sources.libdaemon import log, getPublicIP, daemonize, exiting, Killer
from sources.settings import userKey, devKey, TTS, pasteName
from sources.pastebinAPI import Api

otag = "\x1b[35;1m"
ctag = "\x1b[0m"

if os.getuid():
    home = os.environ['HOME']
    runDir = home + '/.nodns/'
    logFile = home + '/.nodns/nodns.log'
    pidFile = home + '/.nodns/nodns.pid'
    urlFile = home + '/.nodns/nodns.url'
else:
    runDir = '/run/nodns/'
    logFile = '/var/log/nodns'
    pidFile = '/run/nodns/nodns.pid'
    urlFile = '/run/nodns/nodns.url'

if not os.path.isdir(runDir):
    os.mkdir(runDir)

fatal = False

if not devKey:
    log(logFile, 2, "Unique developer API key not found in settings.py, get it from " + otag + "https://pastebin.com/api#1" + ctag)
    fatal = True
if not userKey:
    log(logFile, 2, "User key not found in settings.py, get it from " + otag + "https://pastebin.com/api/api_user_key.html" + ctag)
    fatal = True
if fatal :
    exit(1)
if not pasteName:
    pasteName = os.uname()[1]
    log(logFile, 1, "Paste name not found in settings.py, default is your system name : " + otag + pasteName + ctag )
if not TTS:
    TTS = 15
    log(logFile, 1, "TTS not foud in settings.py, default is : " + otag + "15" + ctag)

api = Api(devKey, userKey)

daemonize(pidFile, logFile)

log(logFile, 0, """Obtaining our public IP address for the first time...""")

# TODO : (log warning si le serveur openDNS ne retourne pas d'IP - pas d'internet par exemple)

public_ip_adress_ = getPublicIP()
log(logFile, 0, """Public IP address is : {0}""".format(otag+public_ip_adress_+ctag))
log(logFile, 0, """Sending our public IP address to Pastebin...""")
paste_url = api.paste(public_ip_adress_, pasteName).text
with open(urlFile, 'w') as file :
    file.write(paste_url+"\n")
log(logFile, 0, """paste URL is : {0}""".format(otag+paste_url+ctag))

try :
    killer = Killer()
    while True :
        if killer.kill_now:
            exit(0)
        public_ip_adress = getPublicIP()
        if public_ip_adress_ == public_ip_adress :
            public_ip_adress_ = public_ip_adress
            for i in range(60):
                sleep(TTS)
                if killer.kill_now:
                    exit(0)
        else :
            log(logFile, 0, """Public IP address has changed...""")
            log(logFile, 0, """New public IP address is : {0}.""".format(otag+public_ip_adress+ctag))
            public_ip_adress_ = public_ip_adress
            api.delete(paste_url.split(sep="/")[-1])
            log(logFile, 0, "Old paste deleted.")
            log(logFile, 0, """Sending our new public IP address to Pastebin...""")
            paste_url = api.paste(public_ip_adress, pasteName).text
            with open(urlFile, 'w') as file :
                file.write(paste_url+"\n")
            log(logFile, 0, """paste URL is : {0}""".format(otag+paste_url+ctag))
finally :
    exiting(logFile, paste_url, api)
