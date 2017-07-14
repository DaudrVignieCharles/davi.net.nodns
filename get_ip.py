#!/usr/bin/python3
# -*-coding:UTF8 -*

from sys import argv
from xml.etree import ElementTree

from sources.pastebinAPI import Api
from sources.settings_ import devKey, userKey

pasteName = argv[1]

api = Api(devKey, userKey)

paste_list = api.list_paste(100).text
xml = ElementTree.fromstring('<list>' + paste_list + '</list>')
pasteKey = xml.findall(".//paste[paste_title='{0}']/paste_key".format(pasteName))[0].text
print(api.show_paste(pasteKey).text)
