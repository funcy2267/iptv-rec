#!/usr/bin/python3

import sys
import os
import json

ScraperPath = './iptvcat-scraper/'
args = sys.argv

arg_autosort = ''
arg_status = ''
arg_country = ''
arg_liveliness = 0
arg_mbps = 0

i=0
for arg in args:
    if arg == "--name":
        arg_name = args[i+1]
    if arg == "--status":
        arg_status = args[i+1]
    if arg == "--country":
        arg_country = args[i+1]
    if arg == "--liveliness":
        arg_liveliness = int(args[i+1])
    if arg == "--mbps":
        arg_mbps = int(args[i+1])
    if arg == "--autosort":
        arg_autosort = args[i+1]
    if arg == "--output":
        arg_output = args[i+1]
    if arg == "--length":
        arg_length = args[i+1]
    i=i+1

os.system('cd '+ScraperPath+' && ./iptvcat-scraper '+arg_name)
ScrapedData = json.loads(open(ScraperPath+'data/all-streams.json', "r").read())

result = []
for stream in ScrapedData:
    if arg_status in stream['status'] and arg_country in stream['country'] and int(stream['liveliness']) >= arg_liveliness and int(stream['mbps']) >= arg_mbps:
        result = result + [stream]

if arg_autosort != '':
    hv = 0
    hv_index = 0
    for stream in result:
        if int(stream[arg_autosort]) > hv:
            hv = int(stream[arg_autosort])
            result_index = hv_index
        hv_index = hv_index + 1
else:
    separator = ' | '
    i=1
    for stream in result:
        print(str(i)+'.', stream['channel']+separator+"Country: "+stream['country']+separator+"Liveliness: "+str(stream['liveliness'])+separator+"Status: "+stream['status']+separator+"Last checked: "+stream['lastChecked']+separator+"Format: "+stream['format']+separator+"mbps: "+str(stream['mbps']))
        i=i+1
    result_index = int(input('Which stream to use? '))-1

os.system('./iptv-rec.sh '+result[result_index]['link']+' '+arg_output+' '+arg_length)
